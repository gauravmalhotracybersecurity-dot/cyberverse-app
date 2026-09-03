PLANS = {
    "free": {
        "name": "Free",
        "price_inr": 0,
        "period": "month",
        "tagline": "Start practicing out loud",
        "limits": {"interviews_per_month": 3, "resume_reviews_per_month": 3, "mentor_messages_per_day": 10},
        "features": ["Limited AI usage", "Basic tools & daily quiz", "Basic certification roadmap", "Weekly league & XP"]
    },
    "pro": {
        "name": "Pro",
        "price_inr": 499,
        "period": "month",
        "tagline": "For serious job seekers",
        "limits": {"interviews_per_month": 100, "resume_reviews_per_month": 50, "mentor_messages_per_day": 200},
        "features": ["High-usage AI interviews & mentor", "Advanced GRC tools & risk assessments", "Resume builder + interview coach", "Advanced certification roadmaps", "Advanced reports & exports"]
    },
    "premium": {
        "name": "Premium",
        "price_inr": 999,
        "period": "month",
        "tagline": "For GRC professionals & teams",
        "limits": {"interviews_per_month": -1, "resume_reviews_per_month": -1, "mentor_messages_per_day": -1},
        "features": ["Everything in Pro", "Advanced GRC assistant & audit assistance", "Advanced templates (SoA, risk register, policies)", "Career assistance & priority features"]
    }
}
