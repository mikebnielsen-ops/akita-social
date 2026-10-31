# AKITA Sales social playbook

This file tells Claude how to run AKITA Sales' social media every week. The scheduled tasks read it first. Mike's corrections get added here, so it always wins over older habits.

## Who we talk to

Owners, CEOs and sales directors at field marketing, door-to-door, retail promotion and telemarketing companies, mainly in Denmark, Norway, Sweden and the UK. Secondary: in-house field sales teams.

They care about: knowing today's sales today, keeping new reps past week two, locations that don't pay, team leaders drowning in manual reporting, motivation that lasts the whole week, and cost per sale.

## Voice (most important)

Mike's rules: simple, direct, human. Start with a problem the reader already knows from their own day. Solve it. Mention AKITA only as the fix, near the end.

- Short sentences. Plain words. One idea per line.
- Open with a hook line that names a real situation ("It's 4 pm.", "Sunday. 9 pm. Laptop open.").
- Concrete details from the street: reps, team leaders, locations, WhatsApp, Excel, Friday meetings.
- Close with a question or a one-line takeaway. No hard sell.
- English only. No emojis as decoration. No hype words (game-changer, revolutionise, unlock, empower, seamless). No stock AI phrasing. Avoid em dashes.
- 400 to 700 characters for most posts. Hashtags: 3, at the end.
- Never invent numbers, results, customers or quotes. Opinions are fine; fake facts are not.

### Approved examples (week 45)

> It's 4 pm.
> Do you know what your team has sold today?
> Not yesterday. Today.
> If the answer is "I'll know when the team leaders call in tonight", you're running the business on yesterday's news.
> In AKITA every sale shows up the second it's made. Per rep, per team, per location.
> You see who's flying and who needs a call. While there's still time to do something about it.

> Your sales competition ends on Friday.
> But it's over on Tuesday.
> The same top three pull away. Everyone else does the maths and stops trying.
> Try this instead. One rep against one rep. One day. Anyone can win a day.
> We call it a battle. In AKITA reps challenge each other straight from the app.
> Who would you put up against each other on Monday?

Mike rejected an earlier, more polished batch as "not good": too long, too corporate, not creative. Keep it punchy.

## Weekly mix

5 image posts plus 2 Reels per week, Monday to Friday.

| Slot | What | Image |
| --- | --- | --- |
| 2 posts | A problem the buyer knows, AKITA as the fix | Branded card (scripts/render_card.py) |
| 1 post | What AKITA can do: one feature, shown | Edited AKITA screenshot from the demo company. Until demo data exists, a branded card |
| 1 post | Field life at a location (shopping centre location, door-to-door street, event) | AI image made with Canva generate-image. Mark `isAiGenerated: true` on Instagram. Never present it as a real customer or team. No real brands or logos in the image |
| 1 post | Customer quote, only a real one Mike has supplied in writing | Branded quote card. If no real quote is available, use another problem post instead |
| 2 Reels | One of the Reel formats below: always about AKITA, with AI-made reps in the scene | AI-made scenes plus screens from the demo company. Kinetic text from scripts/render_text_reel.py as fallback |

Every post must have an image. No exceptions.

### Launch phase (31 October to 22 November 2026)

Mike's decision, 31 October 2026: post almost every day for the first three weeks so the channels have content quickly. Aim for 10 to 12 pieces a week in total, then return to the normal mix above.

- LinkedIn: at most one post a day (Reels count). Weekdays as normal, plus one on Saturday or Sunday at most.
- Facebook: everything LinkedIn gets, plus weekend posts.
- Instagram: one post every day, Reels included. Two a day is fine on weekends to fill the grid.
- Reels: 3 to 4 a week (Instagram, Facebook, YouTube Shorts, and LinkedIn on days with no other LinkedIn post).
- Extra posts are mostly "what AKITA can do" with screens from `library/screens/`, rendered with `scripts/render_screen_card.py`, and carousels of a flow (one screen per slide). More angles on the topics bank, not weaker posts. The voice rules still apply.
- Weekend times: 10:00, 13:00 and 17:00.

Rotate topics. Don't repeat a hook within 6 weeks. Topics bank: live sales overview, new reps quitting, locations that don't pay, Sunday Excel reporting, competitions that die early, team leader time, morning briefing, cost per sale, client asking "how did the campaign go?", reps who hide, onboarding a new rep, weather and bad days, season finals and divisions, Wall of Fame.

## Reels

Reels are about AKITA. We are the system, not the salespeople. Mike's correction, October 2026: no creator-style rep content (first door, a day in my life, what I earned, street humour). Every Reel shows what AKITA does for a team. Reps can be in it, and they are made with AI.

AKITA comes in early in a Reel, not only at the end. The hook is still a real situation the buyer knows.

| Format | What it looks like |
| --- | --- |
| Sale goes live | An AI rep makes a sale at a location and taps the phone. Cut to AKITA: the sale lands and the numbers move |
| Battle | Two AI reps challenge each other. The score moves in AKITA. One wins, the leaderboard changes |
| The leader's view | An AI team leader or owner looks at a phone at 4 pm and sees today's numbers, per rep, team and location |
| One feature, one point | A short AI scene sets up the problem. AKITA shows the answer: Wall of Fame, competitions, or the locations and expenses report |
| Kinetic text | Moving text from a strong hook. Fallback and cheap baseline to compare against |

Rules for every Reel:

- People in Reels are AI-made. Do not film real reps, customers or passers-by.
- Scenes with people are real video: the people move. Never a zoom on a still image.
- A rep is never alone in a shot. Either the rep is talking with a customer, or two reps are talking or giving a high five. Very important.
- No other people in the background of AI video. They appear from nowhere and walk into walls. Ask for an empty, still background, and check it frame by frame.
- AI people are fictional. Never present one as a real rep, employee or customer. No testimonials, quotes or results from them.
- AI people must not look like a real person. No real brands, logos or workwear in the scene.
- Mark AI content: `isAiGenerated: true` on Instagram, and the matching AI label on any other channel that has one.
- Field marketing, not door-to-door: reps stop people on the street and in shopping centres. Say "location", never "stand".
- Screens come only from the demo company, at calm speed. Never speed a clip up. Reps are shown on phone, leaders on desktop. `library/clips/` and `library/screens/` hold approved material.
- Always subtitles.
- Google Omni Flash (`gemini-omni-1.1-flash`) makes the video, on Mike's own paid Gemini API key. Test one clip and show it to Mike before making more. If the tool fails or the result is not good enough, use Kinetic text and say so in the desk document's `claudeNote`.

Test for 8 weeks: 16 Reels, 4 each of Sale goes live, Battle, The leader's view and One feature, one point. Eight weeks gives a direction, not proof.

Measure who comments, whether owners reply, and whether meetings come. Ask in every meeting where they heard about AKITA. Never judge a Reel by views, and never compare with competitors' view counts: many of those look paid.

Example hooks, approved in week 45:

> It's 4 pm. Do you know what your team has sold today?

> Your sales competition ends on Friday. But it's over on Tuesday.

Do not copy:

- Rep-life creator videos and anything that sounds like a salesperson talking.
- Clips from TV shows or other people's material.
- Get-rich language about what reps can earn.
- Humour that laughs at a customer or a rep.
- Long stunts and long interviews.

## Channels and times (Copenhagen time, Europe/Copenhagen)

- LinkedIn company page: all 5 posts and both Reels.
- Facebook page: all 5 posts and both Reels.
- Instagram (akita.sales): 3 posts per week (Mon, Wed, Fri) and both Reels.
- YouTube Shorts: both Reels (title max 70 chars, madeForKids false, type "short").
- TikTok: not yet connected. Skip until it appears in Metricool.
- Default times: posts 08:30 (Mon, Tue, Thu), 12:00 (Wed), 09:00 (Fri). Reels Tue and Thu 17:00.

## Images and Reels

- Screen cards: `python3 scripts/render_screen_card.py '{"theme":"dark|light","eyebrow":"Topic","l1":"Headline","l2":"Second line","screen":"library/screens/phone-12-my-stats.png","step":"1/6"}' out.png` (step is optional, for carousels). Carousels: format "Carousel", several images in `media`, all sent in Metricool `media` in order.
- Cards: `python3 scripts/render_card.py '{"theme":"dark|light","eyebrow":"Topic","l1":"Hook","l2":"Second line"}' out.png`. Alternate dark and light through the week.
- Kinetic-text Reels: write `reels/<ISO week>/<id>/scenes.json` (scenes of 2.4 to 3.6 s, last scene a takeaway, end card is automatic), render with `python3 scripts/render_text_reel.py scenes.json visual.mp4`, and write `spec.json` with a music prompt. Voice-over is optional: voice "Brian", and the visuals must follow the spoken words (about 2.5 words per second).
- The GitHub Action "Reel audio" adds ElevenLabs music and voice when `spec.json` is pushed, and commits `final.mp4`.
- Instagram audio: if Mike has named an Instagram track (in a desk note or in this file under "Current Instagram tracks"), attach it with `instagramData.audioConfiguration` (audioId = the track name; set `videoVolume` 0 when the Reel has music only). Otherwise use the video's own audio.
- Screenshots: only from the demo company. Never show Frontliner, AM, real people's names or real client logos.
- AI location images: generate in Canva (generate-image, portrait 4:5 if possible), get a download URL (export), then run the "Fetch media" workflow (`gh api -X POST repos/mikebnielsen-ops/akita-social/actions/workflows/fetch-media.yml/dispatches -f ref=main -f inputs[url]=<url> -f inputs[path]=drafts/<week>/<file>.png`), wait for it, pull, and use the file. The workspace itself cannot download from Canva. If any step fails, use a branded card instead and say so in the desk document's `claudeNote`.
- `drafts/` may hold not-yet-approved AI images. Everything else in this repo is approved.

### Current Instagram tracks

(none yet)

## The Content Desk (approval)

- URL: https://claude.ai/artifact/T7CzoczN2rc9eWpxd2X4fB (page source: desk/content-desk.html)
- Collection `posts`, one document per post or Reel, id `w<week>-<nn>-<slug>` (Reels: `w<week>-r<n>-<slug>`).
- Fields: week ("2026-W46"), scheduledAt (ISO with offset, Copenhagen time), channels (linkedin, facebook, instagram, youtube), format ("Image post" or "Reel"), pillar, label, text, hashtags, media [{url, assetId, alt, kind: "image"|"video"}], status, plus Mike's editedText, editedHashtags, note.
- Media for the desk: upload with the Artifact tool (publish, url = desk URL, asset: true) and store `/_blob/<id>` in `media.url`. For Reels, upload the silent `visual.mp4` with kind "video".
- Status flow: pending → approved | changes | rejected. Claude sets scheduled (with plannerUrl, metricoolUuid) and later published.
- Use Mike's `editedText` and `editedHashtags` when present.

## Publishing (after approval only)

Nothing goes public before Mike approves it on the desk. This repo is public, so only approved media is committed here.

1. Fetch the approved media from the desk (Artifact read with `path` = assetId) into `media/<week>/` (images) or `reels/<week>/<id>/` (Reels, with scenes.json and spec.json). Push. For Reels wait for the "Reel audio" run to commit `final.mp4`, then pull.
2. Public URL: `https://raw.githubusercontent.com/mikebnielsen-ops/akita-social/main/<path>`.
3. Schedule with Metricool `createScheduledPost`: blogId 7736058, publicationDate timezone Europe/Copenhagen, text = post text + blank line + hashtags, `linkedinData {type: post}`, `facebookData {type: POST or REEL}`, `instagramData {type: POST or REEL, isAiGenerated}`, `youtubeData {type: short, title, madeForKids: false, privacy: public}`.
4. Update the desk document: status "scheduled", plannerUrl, metricoolUuid, publicMediaUrl.

## Things Claude never does

- Publish or schedule anything that is not approved on the desk.
- Comment, like, DM or follow from any account.
- Invent customer quotes, results or numbers, or use AM as a customer reference (it was Mike's own company).
- Present an AI-made person as a real rep, employee or customer.
- Show data or names from real AKITA customers.
- Post in any language but English.
