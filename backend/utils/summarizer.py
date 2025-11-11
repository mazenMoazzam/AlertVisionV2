def generate_summary(events):
    if not events:
        return "No human activity detected during the analysis period."
    summary = f"{len(events)} human detections occurred during the stream."
    return summary
