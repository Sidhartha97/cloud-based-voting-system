import React from 'react';
import { Authenticator } from '@aws-amplify/ui-react';
import { Routes, Route } from 'react-router-dom';
import VotingPage from './VotingPage';
import Callback from './Callback';
import { ThemeProvider, Theme } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';



const myTheme = {
  name: 'my-theme',
  tokens: {
    colors: {
      brand: {
        primary: { value: '#4a90e2' },
      },
    },
  },
};

function App() {
  return (
    <ThemeProvider theme={myTheme}>
      <Authenticator>
        {({ signOut, user }) => (
          <Routes>
            <Route path="/" element={<VotingPage signOut={signOut} user={user} />} />
            <Route path="/callback" element={<Callback />} />
          </Routes>
        )}
      </Authenticator>
    </ThemeProvider>
  );
}

export default App;
