# Banana Search!

## Inspiration
We were inspired to create Banana Search by the everyday challenges of meal planning and grocery shopping. Food prices have skyrocketed in recent years, and we wanted to find a way for users to budget while cooking the food they want. We noticed that many people struggle to figure out what to cook based on what they already have, and often end up overspending or wasting food. By combining smart recipe generation with real-time grocery price comparisons, we envisioned a tool that not only makes meal planning easier but also saves users money and reduces food waste.

## What It Does
### Generates Recipes:
Users enter a desired dish and receive a detailed recipe, complete with an ingredient list and step-by-step cooking instructions.
Optimizes Grocery Lists:
By uploading an image of their fridge, users can quickly identify which ingredients they are missing for the recipe.
Compares Grocery Prices:
The app allows users to select from multiple local grocery stores to view updated pricing and calculate the total cost for the missing ingredients.
Streamlines Shopping:
Provides an organized, editable shopping list and dynamically calculates totals based on store-specific prices and quantities.
How We Built It
Frontend:
Built with Next.js, React, and TypeScript, ensuring a modern, responsive UI that works across devices.
Authentication:
Integrated Supabase to enable secure user sign-up and login, supporting email/password as well as social providers like Google and GitHub.
API Integration:
Developed custom API endpoints for recipe generation and grocery price optimization. We connected with external grocery APIs to fetch real-time pricing and store data.
State Management:
Leveraged React state and localStorage to persist user data (e.g., missing ingredients, shopping list items) across sessions.
User Interface:
Designed interactive components like editable shopping lists, store selection cards, and dynamic total calculations to provide a seamless user experience.
Challenges We Ran Into
Authentication Complexity:
Integrating multiple authentication methods and managing secure user sessions was a significant challenge.
SSR/Hydration Issues:
Addressing discrepancies between server-rendered HTML and client-side rendering in Next.js required careful debugging.
API Data Normalization:
Dealing with inconsistent data formats from various grocery APIs (different price formats, missing fields, etc.) was complex.
CORS and Asynchronous Responses:
Configuring CORS policies and handling asynchronous API responses correctly demanded extra attention.
User Data Matching:
Ensuring that user-inputted ingredient names correctly match with store-specific ingredient data required robust string normalization and matching logic.
Accomplishments That We're Proud Of
Successfully integrated a modern authentication system with Supabase.
Built a dynamic, responsive UI that seamlessly combines recipe generation, grocery list management, and real-time price comparisons.
Overcame technical challenges related to API integration, CORS, and SSR/hydration issues.
Developed a tool that can potentially save users both time and money by optimizing their shopping lists.
What We Learned
State Management:
The importance of efficient state management and data persistence in dynamic web applications.
SSR and Hydration:
Strategies to resolve server-side rendering and hydration issues in Next.js.
API Integration:
Techniques for integrating and normalizing data from multiple external sources.
CORS & Async Handling:
Best practices for handling cross-origin resource sharing and asynchronous API calls.
User-Centric Design:
How thoughtful UI/UX design can significantly improve user experience and engagement.
What's Next for Banana Search
Expand Store Integration:
Integrate additional grocery stores and provide even more detailed, real-time inventory and pricing data.
Enhanced Personalization:
Improve recipe generation algorithms to better match individual user tastes, dietary needs, and seasonal availability.
Mobile Optimization:
Further refine the responsive design for mobile devices and consider developing a native mobile app.
New Features:
Add features like nutritional information, meal planning tools, and budget tracking to offer a comprehensive food management solution.
User Feedback:
Incorporate feedback from our user community to continuously refine and improve the app.
