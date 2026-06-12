from server import app

print("Registered routes:")
for route in app.routes:
    if hasattr(route, "path"):
        print(f"  {route.methods} - {route.path}")
