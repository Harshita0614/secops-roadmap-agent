from app.agent_logic import run_agent

if __name__ == "__main__":
    report = run_agent()

    print("\n📍 Roadmap Steps:")
    for step in report["roadmap"]:
        print(f"- {step}")

    print(f"\n✅ Current Step: {report['current']}")
    print(f"➡️  Next Step: {report['next']}")
    print(f"📊 Status: {report['status']}")

    print("\n⚠️  Risks:")
    for risk in report['risks']:
        print(f" - {risk}")

    print("\n🛠 Suggestions:")
    for suggestion in report['suggestions']:
        print(f" - {suggestion}")
