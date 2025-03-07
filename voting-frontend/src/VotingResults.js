import React, { useState } from "react";
import { fetchAuthSession } from "@aws-amplify/auth";

function VotingResults() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchResults = async () => {
    setLoading(true);
    try {
      // Fetch the ID Token from Cognito
      const session = await fetchAuthSession();
      const idToken = session.tokens?.idToken?.toString();

      if (!idToken) {
        throw new Error("❌ Missing ID Token. User might not be authenticated.");
      }

      const response = await fetch(
        "https://p8flv0e6k6.execute-api.us-east-1.amazonaws.com/test/getResult",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: idToken, // ✅ Include the Cognito ID Token
          },
        }
      );

      if (!response.ok) {
        throw new Error(`❌ Failed to fetch results: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("🔍 Raw API Response:", data);

      // ✅ Fix: Ensure `data.body` is parsed correctly
      const parsedResults = JSON.parse(data.body);
      console.log("✅ Parsed Results:", parsedResults);

      setResults(parsedResults);
    } catch (error) {
      console.error("❌ Error fetching results:", error);
      alert("Error fetching results. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h2>🗳️ Election Results</h2>
      <button
        onClick={fetchResults}
        disabled={loading}
        style={{
          padding: "10px 20px",
          backgroundColor: "#28a745",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        {loading ? "Loading..." : "Get Results"}
      </button>

      {results.length > 0 ? (
        <table
          style={{
            marginTop: "20px",
            width: "80%",
            marginLeft: "auto",
            marginRight: "auto",
            borderCollapse: "collapse",
          }}
          border="1"
        >
          <thead>
            <tr style={{ backgroundColor: "#007bff", color: "white" }}>
              <th style={{ padding: "10px" }}>Candidate</th>
              <th style={{ padding: "10px" }}>Votes</th>
            </tr>
          </thead>
          <tbody>
            {results.map((candidate) => (
              <tr key={candidate.candidate_id}>
                <td style={{ padding: "10px" }}>{candidate.candidate_name}</td>
                <td style={{ padding: "10px" }}>{candidate.vote_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p style={{ marginTop: "20px", fontSize: "18px", color: "red" }}>
          No results available.
        </p>
      )}
    </div>
  );
}

export default VotingResults;
