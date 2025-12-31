# 🛡️ ScamRay: Multimodal AI Phishing Defense

> **Project for [Insert Hackathon Name]**
> *Protecting users from visual spoofing and zero-day phishing attacks using Google Gemini 2.5.*

## 🚨 The Problem
Traditional antiviruses rely on **blacklist databases**—they only catch known threats. 
Hackers now use **"Quishing" (QR Phishing)** and **Visual Spoofing** (fake Netflix/Microsoft login images) to bypass text-based scanners. 

## 💡 The Solution
**ScamRay** is an **Active Defense System**. It doesn't just warn you; it physically blocks interaction with malicious sites using a protected **Shadow DOM** overlay. It uses **Multimodal AI (Vision + Text)** to "see" the website like a human, detecting fraud even if the text is hidden.

---

## 🌟 Key Features

### 👁️ Multimodal Vision Intelligence ("God Mode")
* Uses **Google Gemini 2.5 Flash** to analyze **real-time screenshots** of the webpage.
* Detects visual brand impersonation (e.g., a fake Microsoft login logo) even if the URL is obfuscated.

### 🕵️‍♂️ Forensic Hacker Reveal
* Inspects the HTML `<form>` actions to identify exactly where the data is being sent.
* **The Reveal:** Displays the attacker's destination server (e.g., `hacker-site.xyz`) directly on the warning screen.

### 🛡️ Active Shadow-DOM Defense
* Injects an isolated **Shadow DOM** overlay with a Z-Index of `2.1 Billion`.
* **Benefit:** Physically prevents users from clicking, typing, or interacting with the malicious page.

### ☁️ Crowdsourced Threat Intelligence
* Integrated with **Google Firebase Firestore**.
* Users can click **"REPORT ATTACK"** to instantly save the confirmed phishing URL to a central cloud database, protecting the community.

---

## 🏗️ Architecture

[Chrome Extension] --(Capture Screenshot)--> [Python Flask Server]
                                                    |
                                          [Google Gemini 2.5 API]
                                          (Analyzes Text + Vision)
                                                    |
[Chrome Extension] <--(Risk Score & Forensics)------'
       |
       |--- [Safe?] --> Unblur Page
       |
       '--- [Malicious?] --> 1. Speak Audio Alert 🔊
                             2. Inject Shadow DOM Block 🛡️
                             3. Save to Firebase (On Report) ☁️

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Chrome Extension Manifest V3)
* **Backend:** Python (Flask), PIL (Image Processing)
* **AI Engine:** Google Gemini 2.5 Flash (Generative AI SDK)
* **Database:** Google Firebase Firestore (NoSQL)

---

## 🚀 How to Run

1.  **Clone the Repo**
    ```bash
    git clone [https://github.com/AvinashTripathi1234/ScamRay.git](https://github.com/AvinashTripathi1234/ScamRay.git)
    ```

2.  **Setup Backend**
    ```bash
    cd server
    pip install -r requirements.txt
    python app1.py
    ```

3.  **Load Extension**
    * Open Chrome -> `chrome://extensions`
    * Enable **Developer Mode**.
    * Click **Load Unpacked** -> Select the folder.

---
*Built with ❤️ for a Safer Internet.*

