// components/Auth.tsx
import React, { useState } from 'react';
import { supabase } from '../lib/supabaseClient';

const Auth: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignUp = async () => {
    const { error, data } = await supabase.auth.signUp({ email, password });
    if (error) {
      alert('Error signing up: ' + error.message);
    } else {
      alert('Sign up successful! Check your email for confirmation.');
    }
  };

  const handleSignIn = async () => {
    const { error, data } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      alert('Error signing in: ' + error.message);
    } else {
      alert('Sign in successful!');
    }
  };

  return (
    <div>
      <input
        type="email"
        placeholder="Email address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignUp}>Sign Up</button>
      <button onClick={handleSignIn}>Sign In</button>
    </div>
  );
};

export default Auth;
