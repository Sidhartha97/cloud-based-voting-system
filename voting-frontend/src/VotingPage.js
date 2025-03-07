import React, { useState, useEffect } from "react";
import { Amplify } from "aws-amplify";
import { fetchAuthSession, getCurrentUser, signOut } from "@aws-amplify/auth";
import awsmobile from "./aws-exports";
import VotingResults from "./VotingResults";
import "./VotingPage.css"; // Import CSS file

Amplify.configure(awsmobile);

function VotingPage({ user }) {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCandidates();
    fetchUserId();
  }, []);

  const fetchUserId = async () => {
    try {
      const currentUser = await getCurrentUser();
      if (currentUser) {
        setUserId(currentUser.username);
      }
    } catch (error) {
      console.error("❌ Error fetching user ID:", error);
    }
  };

  const fetchCandidates = async () => {
    try {
      const idToken = await fetchIdToken();
      if (!idToken) {
        console.error("❌ Missing ID Token");
        return;
      }

      const response = await fetch(
        "https://p8flv0e6k6.execute-api.us-east-1.amazonaws.com/test/candidates",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: idToken,
          },
        }
      );

      const data = await response.json();
      const candidates = typeof data.body === "string" ? JSON.parse(data.body) : data.body;

      if (Array.isArray(candidates)) {
        setCandidates(candidates);
      } else {
        console.error("⚠️ Invalid candidates format:", candidates);
        setCandidates([]);
      }
    } catch (error) {
      console.error("❌ Error fetching candidates:", error);
    }
  };

  const fetchIdToken = async () => {
    try {
      const session = await fetchAuthSession();
      return session.tokens?.idToken?.toString() ?? null;
    } catch (error) {
      console.error("❌ Error fetching ID Token:", error);
      return null;
    }
  };

  const handleVote = async () => {
    if (!userId || !selectedCandidate) {
      alert("Please select a candidate before submitting your vote.");
      return;
    }

    setLoading(true);

    const voteData = {
      user_id: userId,
      candidate_id: selectedCandidate,
    };

    try {
      const idToken = await fetchIdToken();
      if (!idToken) {
        console.error("❌ Missing ID Token");
        setLoading(false);
        return;
      }

      const response = await fetch(
        "https://p8flv0e6k6.execute-api.us-east-1.amazonaws.com/test/votes",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: idToken,
          },
          body: JSON.stringify(voteData),
        }
      );

      const data = await response.json();
      if (!response.ok || (data.status && data.status.toLowerCase() === "error")) {
        alert(data.message || "An error occurred");
        return;
      }

      alert("✅ Vote submitted successfully!");
    } catch (error) {
      alert("Error submitting vote. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="voting-container">
      <h1>🗳️ Voting System</h1>
      <p>Welcome, {user.username}!</p>

      <h2>Candidates</h2>
      {candidates.length > 0 ? (
        <ul className="candidate-list">
          {candidates.map((candidate) => (
            <li
              key={candidate.candidate_id}
              className={selectedCandidate === candidate.candidate_id ? "selected" : ""}
              onClick={() => setSelectedCandidate(candidate.candidate_id)}
            >
              {candidate.candidate_name} ({candidate.party})
            </li>
          ))}
        </ul>
      ) : (
        <p>No candidates available.</p>
      )}

      <button
        onClick={handleVote}
        disabled={!selectedCandidate || loading}
        className="vote-btn"
      >
        {loading ? "Submitting..." : "Submit Vote"}
      </button>

      <button onClick={signOut} className="logout-btn">
        Logout
      </button>

      <hr />

      <VotingResults />
    </div>
  );
}

export default VotingPage;
