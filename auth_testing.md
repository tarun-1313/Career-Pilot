# Auth-Gated App Testing Playbook (Emergent Google OAuth)

## Step 1: Create Test User & Session
```bash
mongosh --eval "
use('test_database');
var userId = 'user_test_' + Date.now();
var sessionToken = 'test_session_' + Date.now();
db.users.insertOne({
  user_id: userId,
  email: 'test.user.' + Date.now() + '@example.com',
  name: 'Test User',
  picture: 'https://via.placeholder.com/150',
  created_at: new Date(),
  onboarded: false,
  skills: [],
  interests: []
});
db.user_sessions.insertOne({
  user_id: userId,
  session_token: sessionToken,
  expires_at: new Date(Date.now() + 7*24*60*60*1000),
  created_at: new Date()
});
print('session_token=' + sessionToken);
print('user_id=' + userId);
"
```

## Step 2: API smoke
```bash
curl -i "$BACKEND_URL/api/auth/me" -H "Authorization: Bearer $SESSION_TOKEN"
```

## Step 3: Browser cookie
```python
await page.context.add_cookies([{
    "name": "session_token",
    "value": SESSION_TOKEN,
    "domain": "career-pilot-14.preview.emergentagent.com",
    "path": "/",
    "httpOnly": True,
    "secure": True,
    "sameSite": "None",
}])
```
