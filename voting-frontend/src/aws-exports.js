const awsmobile = {
    aws_project_region: 'us-east-1',
    aws_cognito_region: 'us-east-1',
    aws_user_pools_id: 'us-east-1_qlIRk19WN',
    aws_user_pools_web_client_id: '3bhf4leibl693s7c0ckefus5s7',
    oauth: {
        domain: 'us-east-1qlirk19wn.auth.us-east-1.amazoncognito.com',
        scope: ['phone', 'email', 'openid', 'profile', 'aws.cognito.signin.user.admin'],
        redirectSignIn: 'http://localhost:3000/callback',
        redirectSignOut: 'http://localhost:3000',
        responseType: 'code',
    },
    aws_cognito_authenticationFlowType: 'USER_SRP_AUTH',  // ✅ Add this if missing
};

export default awsmobile;
