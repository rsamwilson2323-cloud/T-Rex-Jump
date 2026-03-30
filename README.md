# 🦖 T-Rex Jump Game (Python + Pygame)

A clean and fun recreation of the classic Google Chrome Dino game built using **Python** and **Pygame**.  
Jump over obstacles, duck birds, and survive as long as possible while your speed increases!

---

## 🚀 Features

- 🦖 Smooth Dino character with jump & duck mechanics  
- 🌵 Random cactus obstacles  
- 🐦 Flying birds with different heights  
- ☁ Animated moving clouds  
- 🌗 Day & Night background switching  
- 📈 Increasing difficulty (speed increases over time)  
- 🏆 High score system (saved locally)  
- 🎮 Simple controls (easy to play)

---

## 📁 Project Structure

```
T-Rex-Jump/
│
├── T-Rex jump.py              # Main game file
├── T-Rex jump google hack code.txt
├── highscore.txt              # Stores high score
├── README.md                  # Project documentation
└── LICENSE
```

---

## ⚙️ Requirements

Make sure you have Python installed.

Install required library:

```bash
pip install pygame
```

---

## ▶️ How to Run

```bash
python "T-Rex jump.py"
```

---

## 🎮 Controls

| Key            | Action          |
|----------------|----------------|
| SPACE / ↑      | Jump           |
| ↓              | Duck           |
| SPACE / ↑      | Restart (after Game Over) |

---

## 🧠 Game Logic

- Only **one obstacle at a time** (clean gameplay)
- Obstacles include:
  - 🌵 Cactus (jump to avoid)
  - 🐦 Bird (duck to avoid)
- Speed increases as score increases
- Score increases when you successfully pass obstacles
- High score is saved in `highscore.txt`

---

## 📊 Gameplay Mechanics

- Gravity-based jumping system  
- Collision detection using rectangles  
- Procedural obstacle spawning  
- Dynamic background switching (day/night cycle)

---

## 🖼️ Graphics

- Fully drawn using **Pygame shapes**
- No external images required
- Lightweight and fast

---

## 💾 High Score System

- Automatically saves your highest score
- Stored locally in:

```
highscore.txt
```

---

## 🛠️ Customization Ideas

You can easily extend this project:

- Add sound effects 🔊  
- Add animations or sprites 🎨  
- Add multiple obstacles at once ⚡  
- Add pause menu ⏸️  
- Add mobile controls 📱  

---

## 📜 License

This project is licensed under the terms of the included LICENSE file.

---

## 👨‍💻 Author

**Sam Wilson**  

🌐 GitHub https://github.com/rsamwilson2323-cloud

💼 LinkedIn https://www.linkedin.com/in/sam-wilson-14b554385

---

## ⭐ Support

If you like this project:

- ⭐ Star the repository  
- 🍴 Fork it  
- 🚀 Share with others  

---

## 🎯 Final Note

This project is a great beginner-friendly example of:

- Game development using Python  
- Working with Pygame  
- Object-oriented programming  
- Real-time event handling  

Enjoy building and playing! 🦖🔥
