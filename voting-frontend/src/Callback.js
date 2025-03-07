import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '@aws-amplify/auth';

function Callback() {
  const navigate = useNavigate();

  useEffect(() => {
    getCurrentUser()
      .then(() => navigate('/'))
      .catch((err) => console.error("Authentication error:", err));
  }, [navigate]);

  return <div>Loading...</div>;
}

export default Callback;
