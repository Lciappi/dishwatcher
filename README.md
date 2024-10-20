# dishwatcher
Notify roomates of dirty dishes

## Inspiration
You move out of your parents home and you realize… the dishes don’t clean themselves. Unfortunately, some of our roommates haven’t come to that conclusion yet. If only there was a way to remind them so they don’t fork-get...

Inspired by the frustrations of communal living, we created an app to track who leaves dishes and who cleans them up. Dish it out, clean it up!

## What it does
DishWatcher is an app that uses computer vision to detect when dishes are left in the sink or cleaned. It then sends real-time notifications to the appropriate roommate, promoting accountability and fostering a cleaner living environment.

Key features include:

- Real-time notifications: Receive instant alerts when dishes are left or cleaned.
- Leaderboard: Track the cleanliness of each roommate and identify the top contributors.
- Visual evidence: Capture photos or videos of dish-drop-off moments for added accountability.
- By using DishWatcher, you can:

  - Reduce arguments: Resolve disputes over chores with clear evidence.
  - Promote fairness: Ensure that everyone contributes to keeping the space clean.
  - Create a more harmonious living environment.

## How we built it
Our tech stack includes:

- Frontend: Javascript, React
- Backend: Python, Flask
- Machine learning models: OpenCV for facial recognition, YOLO for object recognition

## Challenges we ran into
Recognizing dishes with a high accuracy is surprisingly challenging! Objects often flickered in and out of view, and labels changed due to low confidence. We addressed this by implementing a prediction buffer to make our app more robust.

Integrating SocketIO for real-time updates also presented challenges.

## Accomplishments that we're proud of
As a two-person team, we're incredibly proud of completing DishWatcher within the hackathon timeframe. We worked tirelessly to deliver a functional app with all the core features we envisioned.

We're also excited about our experience with OpenCV and YOLO. Incorporating these machine learning models was a valuable learning experience.

## What we learned
1. A two-person team is possible, but not recommended.
2. Bring Coke Zero from home so that we don't have to spend $15+ funding our addictions from vending machines.

## What's next for DishWatcher
1. Fine tune model
2. Add pictures of the dish-drop-off moment onto the hall of shame
3. Add video of the camera view onto the website
