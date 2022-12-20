from expense_tracker import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)


from expense_tracker.routes import (
    user_routes,
    goal_routes,
    budget_routes,
    expenses_routes
)