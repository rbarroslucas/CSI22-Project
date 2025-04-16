# CSI22 Project

This repo contains our project developed as part of the first module of CSI-22. This 2D game captures the feeling of our nightmarish return to university once again. You play as two characters, trapped in a nightmare. Your mission is to escape by clearing a series of rooms—each with increasing difficulty, hidden weapons, and multiple enemies. 

Team:

 Diogo Bueno Rodrigues
 
 Daniel da Silveira Sahadi
 
 Lucas Ribeiro do Rêgo Barros
 
 Luiz Felipe de Brito Ramos
 
 Thiago Galante Pereira

 #### How to run:
 In order to play the game, first thing needed is to create a environmet with the requirements, which can be found in the repo as well.
 Using conda:
```cpp
conda create -n env python=3.12
conda activate env
conda install pip
pip install pygame pytmx
python .\src\main.py
```

 Uing venv

 # 🎮 CSI22 Project – *Bad Trip*

This repository contains our project developed as part of the first module of **CSI-22**.  
This 2D game captures the feeling of our **nightmarish return to university** once again.

You play as **two characters**, trapped in a nightmare. Your mission is to **escape** by clearing a series of rooms—each with increasing difficulty, hidden weapons, and multiple enemies.

---

## 🧠 Game Concept

- ⚔️ Defeat bosses across different rooms.
- 🔍 Explore to find hidden weapons and solve puzzles.
- 💀 Survive with only **three lives** per character.
- 👻 Switch between characters and use ghost form for exploration.
- 🧩 Discover secret areas and false walls to gain the upper hand.

---

## 🎮 Controls

| Action               | Key(s)             |
|----------------------|--------------------|
| Move                 | `W`, `A`, `S`, `D`  |
| Use Potion (1–3)     | `1`, `2`, `3`       |
| Shoot Projectile     | `J`                |
| Summon Ghost         | `K`                |
| Switch Characters    | `SPACE`            |

---

## 🛠️ How to Run

To play the game, first set up a Python environment with the required dependencies.  
You can use either **Conda** or **venv**.

### 🔹 Using Conda

```bash
conda create -n env python=3.12
conda activate env
conda install pip
pip install pygame pytmx
python ./src/main.py
```
### 🔹 Using venv

```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

pip install pygame pytmx
python ./src/main.py
```

