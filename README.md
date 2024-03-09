# Pemanfaatan Algoritma Greedy dalam Pembuatan Bot Permainan Diamonds
> Evelyn Yosiana - 13522083
>
> Fedrianz Dharma - 13522090
>
> Steven Tjhia - 13522103


## Table of Contents
* [General Info](#general-information)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)


## General Information
- This project aims to solve Diamonds by _Greedy_ Algorithm. The game aims to get as much diamond as you can.


## Setup

### How to Run Game Engine

#### a. Install Requirements

- Node.js (https://nodejs.org/en) 
- Docker desktop (https://www.docker.com/products/docker-desktop/) 
- Yarn

    `npm install --global yarn`

#### b. Install and Configure Game Engine

1. Download source code (.zip) from (https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)

2. Extract zip and go to the directory where you extract it and open the terminal.

3. Go to project root directory and then do:

    `cd tubes1-IF2110-game-engine-1.1.0`

4. Install dependencies with Yarn

    `yarn`

5. Setup default environment variable

- Windows

    `./scripts/copy-env.bat`

- Linux / (possibly) MacOS

    `chmod +x ./scripts/copy-env.sh`

    `./scripts/copy-env.sh`

6. Setup local database (open docker desktop first)

    `docker compose up -d database`

- Windows

    `./scripts/setup-db-prisma.bat`

- Linux / (possibly) MacOS

    `chmod +x ./scripts/setup-db-prisma.sh`

    `./scripts/setup-db-prisma.sh`

#### c. Build

    `npm run build`
    
#### d. Run

    `npm run start`

### How to Run Bots

#### a. Install Requirements

#### b. Install and Configure Bot Engine

#### c. Run


## Usage
1. JELASIN CARA EDIT IMPLEMENTASI DI BOT NYA
2. Buat file python baru pada direktori /game/logic
3. Buatlah kelas baru yang meng-Inherit kelas BaseLogic, lalu implementasikan constructor dan method next_move pada kelas tersebut.
4. Next_move akan mengembalikan nilai delta_x dan delta_y, dimana nilai yang diperbolehkan hanyalah (1, 0), (0, 1), (-1, 0), (0, -1). Apabila nilai ilegal atau di-luar range board, maka move akan diabaikan oleh program.
5. Import kelas yang telah dibuat pada main.py dan daftarkan pada dictionary CONTROLLERS
6. Jalankan game engine dan sesuaikan argumen logic pada command menjadi nama bot yang telah terdaftar pada CONTROLLERS. Anda dapat menjalankan satu bot saja atau beberapa bot menggunakan .bat atau .sh script.

### Scripts

    `python main.py --logic <nama bot yang dijalankan> --email=your_email@example.com --name=your_name --password=your_password --team etimo`

## Project Status
Project is: _complete_.


## Room for Improvement
- Advanced tackle mechanism
- Escape mechanism
- Revenge mechanism
