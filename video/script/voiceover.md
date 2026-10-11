# Base activa restaurada — v05

2026-10-10: el propietario pide recuperar la conversación pausada anterior. Base activa: conversación v02 de 50 s, con los IDs elegidos de madre e hija, pausas y filtro telefónico. Se descarta como base la toma corta v03. Corregir solo entonaciones concretas tras identificarlas. La sincronía y transformación del logo v04 siguen pendientes; no se consideran aprobadas.

# Actualización activa — 2026-10-10, v04

Nueva prueba tras rechazo de voces robóticas: `opening-dialogue-v03.request.json` y `brand-narration-v02.request.json`. Sin etiquetas de lentitud ni atempo; conversación intacta sin pausas añadidas. Filtro telefónico común a madre e hija. George sigue provisional. Prevalece sobre instrucciones históricas de estirar a 50 s. Escucha pendiente.

# VoxWave — Background phone conversation

Updated: 2026-10-09. Active dialogue proposal for the 50-second opening in cinematic-prompt-script-v03.md. Supersedes the earlier father/daughter and book/weather scratch scripts. The owner requested a coherent call with a beginning and ending, possibly mentioning a medical appointment. Exact dialogue and performance remain proposed; no audio has been generated.

## Purpose and delivery
Latest owner direction, 2026-10-10: the 50-second duration is a guide, not a hard target. The CALL MUST END BEFORE THE LOGO TRANSITION. This overrides earlier farewell-over-logo instructions below. Keep current audio temporarily; unusual intonations and artificial pauses are known and deferred for later review. Compare farewell before the final question versus during it, and lower dialogue prominence. Animatic v02 keeps existing speech ending at 49.75 s, with logo handoff starting at 56.55 s.


Latest casting update, 2026-10-10: daughter is now `ogwqBH5bbF03DSbNiRNN`, replacing Sarah at the owner's request. Mother remains `5u41aNhyCU6hXOcjPPv0`. Active audio is `opening-dialogue-v02-preview-50s.mp3` in video/renders; actual cues and RMS data are in `opening-dialogue-v02-edit.json`. This replaces v01 as the working audio. Final interpretation still awaits listening review.

Production update, 2026-10-10: owner approved casting test v02. Full dialogue generated using `opening-dialogue-v01.request.json`; original MP3 is 34.88 s. Local edit is exactly 50 s (WAV): 3 s lead, pitch-preserving tempo factor 0.92, measured inter-turn pauses and 0.25 s final tail. The final turn ends at 49.75 s. Actual cues in `video/renders/opening-dialogue-v01-edit.json` supersede the approximate table below. Both voices receive the same 300–3400 Hz telephone filter. Preview includes a provisional locally synthesized ring; final ring/pickup must follow the generated shot. The dialogue-only filtered master provides the real RMS waveform data; the ring does not drive it. Final audio performance still requires listening review.

Owner direction, 2026-10-10: replace Julie with ElevenLabs voice `5u41aNhyCU6hXOcjPPv0` for the mother. Keep Sarah as the current daughter candidate. The final conversation must be more unhurried and nuanced than casting test v01: brief listening pauses, a thoughtful beat before the mother's response, warmth when asking about her daughter, and understated reassurance. Avoid uniform slow motion, theatrical sadness or exaggerated frailty. Apply the same telephone treatment to BOTH speakers for the whole call. Keep the clean master for editing. The 50-second scene target remains; adjust pauses in the final edit rather than assuming a generated take has the desired timing.

A daughter calls to ask how her mother is feeling. They discuss a pending medical appointment. The daughter has to return to work and arranges to call again that evening, giving the conversation a motivated ending. The owner rejected the breakfast version and requested a 50-second call; no breakfast dialogue remains. The final goodbye may overlap the logo reveal so the opening stays within 50 seconds.

Both voices are original fictional AI voices, speaking natural English. Mother: older, warm and matter-of-fact; no exaggerated frailty, breathlessness or vocal symptom imitation. Daughter: adult, familiar and attentive, not a presenter or clinician. No need to impose a caricatured Baltic accent. The English-language call is part of the creative presentation.

The caller does not name Parkinson's or repeat the title-card statistics. The appointment and callback are fictional everyday details, not evidence of real waiting times or an actual case. No diagnosis, test result or guaranteed appointment date is invented.

## Proposed dialogue and approximate cues

Target: a 50-second audio scene including the short ring, pickup and natural pauses. These are approximate delivery windows, not measured timings. Generate a natural take and edit pauses to fit without cutting the farewell. Speech continues during the final graphic transition; this replaces the earlier stop at 43 seconds. The roughly 105-word dialogue should be tried at an ordinary conversational pace before exact timing is locked.

| Time | Speaker / sound | Exact proposed line |
|---|---|---|
| 00:00-00:03 | Sound | Brief generic feature-phone ring and pickup. |
| 00:03-00:04 | Mother | "Hello?" |
| 00:04-00:08 | Daughter | "Hi, Mum. It's me. How are you feeling today?" |
| 00:08-00:13 | Mother | "Oh, I'm all right. A little tired, that's all. How are you?" |
| 00:13-00:20 | Daughter | "I'm okay. Busy at work. Did you manage to call the doctor?" |
| 00:20-00:26 | Mother | "Yes, yesterday. They're going to call me back with an appointment." |
| 00:26-00:32 | Daughter | "Let me know when you hear. I'll see if I can come with you." |
| 00:32-00:35 | Mother | "That would be lovely." |
| 00:35-00:43 | Daughter | "Listen, I'd better get back to work. Can I call you this evening?" |
| 00:43-00:45 | Mother | "Of course, love." |
| 00:45-00:48 | Daughter | "All right. Speak tonight. Love you." |
| 00:48-00:50 | Mother | "Love you too. Bye." |

## Copy-ready voice generation prompt

```text
Generate a brief, coherent English phone conversation between an older mother and her adult daughter. Use two original fictional female voices. They know each other well. The mood is ordinary, warm and understated, with a small note of reassurance when the daughter offers to come to the appointment. The mother speaks with agency and natural warmth. The daughter is attentive without sounding anxious or patronising.

Use conversational delivery, natural breaths and gentle pauses. The daughter is making a short call during a work break; her return to work motivates the ending without sounding dismissive or rushed. No narration, crying, whispering, theatrical sadness, exaggerated elderly voice, disease-related vocal impairment, music or sound effects. Do not imitate a real person. Deliver clean unfiltered voices, preferably separate speaker tracks, with room for editing. Target approximately 47 seconds of dialogue including pauses, for a 50-second scene with the short opening ring and pickup. Timing must be measured and adjusted after generation; do not cut off the last line. Speak only the dialogue, not the speaker labels.

Mother: Hello?
Daughter: Hi, Mum. It's me. How are you feeling today?
Mother: Oh, I'm all right. A little tired, that's all. How are you?
Daughter: I'm okay. Busy at work. Did you manage to call the doctor?
Mother: Yes, yesterday. They're going to call me back with an appointment.
Daughter: Let me know when you hear. I'll see if I can come with you.
Mother: That would be lovely.
Daughter: Listen, I'd better get back to work. Can I call you this evening?
Mother: Of course, love.
Daughter: All right. Speak tonight. Love you.
Mother: Love you too. Bye.
```

## Mix and waveform instructions

- Keep the ring brief and restrained; do not reuse a branded Nokia melody by default. Synchronise pickup to the generated hand action rather than forcing it to an unverified frame.
- Apply a light telephone filter to a copy of the clean speech. The call is audible but remains below the text-reading task throughout; no foreground narrator.
- Keep the same call timeline across home, road, clinic and black cards. The voices are an editorial sound bridge, not physical speech occurring in the clinic.
- Drive waveform movement from the synthetic dialogue before the final background volume reduction; preserve real pauses. Do not keep a speech-like loop running after the goodbye.
- During the final question (00:39-00:44), the daughter is arranging the evening call. Keep this exchange low; do not emphasise it over the main text.
- At 00:44-00:45 the waveform is still audio-reactive. From 00:45 it becomes deliberate graphic motion for the logo, while the final goodbye continues quietly. End the call naturally by 00:50, without a busy tone or an abrupt fade mid-word. This supersedes the previous instruction to finish speech before the morph.
- Check intelligibility and overall pacing after generation; the duration in this document is a target, not a measured result.
