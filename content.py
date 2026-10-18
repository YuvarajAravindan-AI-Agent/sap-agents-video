"""Scenes for the 'SAP Agents - governed' demo video. Each sentence: (on-screen caption, spoken text)."""
VOICE = "Sulafat"
SCENES = [
 dict(id="banner", nav="Banner", sentences=[
  ("SAP agents are only useful if you can trust their answers.",) * 2,
  ("This demo shows an SAP agent that cannot do its own arithmetic, cannot hide a call, and leaves an audit trail for every question it answers.",) * 2]),
 dict(id="standard", nav="Problem", sentences=[
  ("First, how the standard build is put together in Joule Studio.",) * 2,
  ("A destination variable points the agent at the maintenance order service.",) * 2,
  ("Then one Joule skill is created for each service operation.",) * 2,
  ("Finally five tools are attached to a single agent, and the model decides how to chain them.",) * 2]),
 dict(id="problem", nav="Problem", sentences=[
  ("We started with a Joule agent built the standard way, from the SAP learning journey.",) * 2,
  ("Asked whether a maintenance order was ready, it looked up the order, its operations, the components and the stock, and then let the language model do the maths.",) * 2,
  ("For material 41, the data said 1.7 required and 500 available.",
   "For material forty-one, the data said one point seven required and five hundred available."),
  ("The agent still reported a shortage of 1.2 units, and the debug logs could not show why.",
   "The agent still reported a shortage of one point two units, and the debug logs could not show why.")]),
 dict(id="workflow", nav="Idea", sentences=[
  ("The fix is a change of responsibility.",) * 2,
  ("The language model understands the question and writes the answer, but it never calculates.",) * 2,
  ("Every number comes from a governed service, built with the SAP Cloud Application Programming model on SAP HANA Cloud.",) * 2,
  ("The service sums stock across storage locations in code, returns a verdict for each material, and writes an audit row for the call.",) * 2]),
 dict(id="live", nav="Live", sentences=[
  ("Here is the live agent, running on SAP BTP.",) * 2,
  ("Asked whether order 1000001 is ready, it makes one governed tool call, validate order stock.",
   "Asked whether order one million and one is ready, it makes one governed tool call, validate order stock."),
  ("Material 41 is sufficient. Material 42 is short by 1.2.",
   "Material forty-one is sufficient. Material forty-two is short by one point two."),
  ("The conversation ID on screen ties this chat to its audit trail.",
   "The conversation I D on screen ties this chat to its audit trail.")]),
 dict(id="architecture", nav="Architecture", sentences=[
  ("The architecture has five parts, all on SAP BTP except the language model.",) * 2,
  ("A small chat application runs on Cloud Foundry and holds the tool loop.",) * 2,
  ("It finds the stock service through the Destination service, which hands it an OAuth token with the agent scope.",) * 2,
  ("The CAP service validates that token, runs the lookup on SAP HANA Cloud, and writes the audit row.",
   "The C A P service validates that token, runs the lookup on SAP HANA Cloud, and writes the audit row."),
  ("Only the language model is outside SAP, and it only ever sees tool results, never the database.",) * 2]),
 dict(id="built", nav="Built live", sentences=[
  ("Everything here was built live on a personal SAP BTP trial account.",) * 2,
  ("A free-tier SAP HANA Cloud instance, a Business Application Studio dev space, an MTA build and a Cloud Foundry deployment.",
   "A free-tier SAP HANA Cloud instance, a Business Application Studio dev space, an M T A build and a Cloud Foundry deployment."),
  ("And the destination, registered in the cockpit.",) * 2]),
 dict(id="verified", nav="Verified", sentences=[
  ("These are results from the deployed service on SAP HANA Cloud, called with a real OAuth token.",) * 2,
  ("Order 1000001 returns the verdict shortage.",
   "Order one million and one returns the verdict shortage."),
  ("Material 41 needs 1.7 and has 500. Material 42 needs 10 and has 8.8.",
   "Material forty-one needs one point seven and has five hundred. Material forty-two needs ten and has eight point eight."),
  ("The destination was created and tested with a token fetched through the Destination service.",) * 2]),
 dict(id="seq1", nav="Sequence", sentences=[
  ("This sequence shows one question from start to finish.",) * 2,
  ("The user asks. The app sends the question and the tool list to the model, which chooses validate order stock.",) * 2,
  ("The app gets a token from the Destination service and calls the CAP service with the conversation ID.",
   "The app gets a token from the Destination service and calls the C A P service with the conversation I D."),
  ("The service reads HANA, computes the verdict in code, inserts the audit row, and returns the result.",) * 2,
  ("The model only phrases what the tool returned.",) * 2]),
 dict(id="seq2", nav="Failures", sentences=[
  ("Failures are evidence too.",) * 2,
  ("A call without a token is rejected with 401 and recorded as denied.",
   "A call without a token is rejected with four oh one and recorded as denied."),
  ("A caller with the wrong scope gets 403, also recorded.",
   "A caller with the wrong scope gets four oh three, also recorded."),
  ("An unknown order returns 404, and that is recorded after the rollback, so the failed attempt still leaves a row.",
   "An unknown order returns four oh four, and that is recorded after the rollback, so the failed attempt still leaves a row.")]),
 dict(id="evidence", nav="Evidence", sentences=[
  ("These are the rows read back from SAP HANA Cloud after the live run.",) * 2,
  ("Each row names the tool, the outcome, the status code, and the conversation it belongs to.",) * 2,
  ("Including the conversation from the browser chat you saw earlier.",) * 2]),
 dict(id="difference", nav="Difference", sentences=[
  ("How is this different from conservative SAP?",) * 2,
  ("Conservatively, a person navigates transactions or apps to the order, its components and the stock, and compares the numbers by eye. The logic sits in transactions and in judgment, and the audit trail is in change documents and logs that are not tied to the question that was asked.",) * 2,
  ("Here, you ask in plain language. The agent chains the lookups, but a tested service function computes the verdict, and every call, allowed or denied, is recorded against the conversation.",) * 2,
  ("What stays the same is the SAP foundation: HANA, BTP and the SAP security model. What changes is who joins the dots, where the arithmetic lives, and how provable the answer is.",) * 2]),
 dict(id="limits", nav="Limits", sentences=[
  ("A few honest limits.",) * 2,
  ("This runs on sample data in a trial account, standing in for an S/4HANA backend.",
   "This runs on sample data in a trial account, standing in for an S four HANA backend."),
  ("The language model is not an SAP model, so real regulated data would need an approved one.",) * 2,
  ("Next: real SAP APIs through the destination, an audit dashboard, and a model inside your approved boundary.",) * 2]),
 dict(id="about", nav="About", sentences=[
  ("I'm Yuvaraj Aravindan, founder of AI Agentic Enterprises. We build governed AI agents for regulated industries on enterprise platforms like SAP.",) * 2,
  ("This was an independent demonstration on an SAP BTP trial account, not an SAP product announcement.",) * 2]),
]
