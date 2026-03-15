import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit Sayfa Ayarları (Tam Ekran Modu)
st.set_page_config(
    page_title="Işık Akışı: Tutulma",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Streamlit'in varsayılan menülerini ve boşluklarını gizleyen CSS
st.markdown("""
    <style>
        /* Ana bloğun boşluklarını sıfırla */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        /* Üst menüyü ve alt bilgiyi gizle */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        /* iframe'in scroll bar çıkarmasını engelle */
        iframe {
            border: none;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Oyunun Tüm HTML, CSS ve JavaScript Kodları
html_code = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Işık Akışı: Tutulma</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500&display=swap');

        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #050510;
            font-family: 'Quicksand', sans-serif;
            touch-action: none;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }

        #gameCanvas {
            display: block;
            width: 100%;
            height: 100%;
        }

        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .timer-display {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.5rem;
            font-weight: 500;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
            margin-bottom: 10px;
            font-variant-numeric: tabular-nums;
        }

        .light-bar-container {
            width: 200px;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            opacity: 0;
            transition: opacity 1s ease;
        }

        .light-bar-fill {
            height: 100%;
            width: 100%;
            background: linear-gradient(90deg, #69D2E7, #ffffff);
            box-shadow: 0 0 10px #ffffff;
            transition: width 0.2s ease-out;
        }

        #sound-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            color: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            pointer-events: auto;
            transition: all 0.3s;
            font-size: 1.2rem;
            background: rgba(0,0,0,0.2);
            z-index: 20;
            -webkit-tap-highlight-color: transparent;
        }
        
        #sound-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }

        #start-screen, #game-over-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(5, 5, 16, 0.8);
            backdrop-filter: blur(8px);
            z-index: 10;
            transition: opacity 0.8s ease;
        }

        #game-over-screen {
            display: none;
            opacity: 0;
            background: rgba(0, 0, 0, 0.95);
        }

        h1 {
            color: white;
            font-weight: 300;
            letter-spacing: 5px;
            margin-bottom: 10px;
            text-align: center;
            text-shadow: 0 0 20px rgba(100, 200, 255, 0.5);
        }

        p {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            margin-top: 0;
            text-align: center;
            max-width: 80%;
            line-height: 1.5;
        }

        .pulse-text {
            margin-top: 40px;
            color: rgba(255, 255, 255, 0.9);
            animation: pulse 3s infinite ease-in-out;
            cursor: pointer;
            padding: 15px 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.05);
            pointer-events: auto;
            -webkit-tap-highlight-color: transparent;
        }

        .stat-value {
            font-size: 2rem;
            color: #69D2E7;
            margin: 20px 0;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.7; }
        }

        #vignette {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background: radial-gradient(circle, transparent 50%, rgba(0,0,0,0.8) 120%);
            transition: background 0.5s ease;
            z-index: 2;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas"></canvas>
        <div id="vignette"></div>
        
        <div id="ui-layer">
            <div id="sound-btn" onclick="toggleMute()">🔊</div>
            <div class="timer-display" id="timer-display">00:00</div>
            <div class="light-bar-container" id="light-bar-container">
                <div class="light-bar-fill" id="light-bar"></div>
            </div>
        </div>

        <div id="start-screen">
            <h1>IŞIK TUTULMASI</h1>
            <p>Işığını koru. Karanlık artıyor.<br>Sadece gerekli sesler.</p>
            <div class="pulse-text" onclick="startGame()">Aydınlat</div>
        </div>

        <div id="game-over-screen">
            <h1>KARANLIK</h1>
            <p>Işık tamamen söndü.</p>
            <div class="stat-value" id="final-time">00:00</div>
            <div class="pulse-text" onclick="resetGame()">Yeniden Dene</div>
        </div>
    </div>

    <script>
        const config = {
            particleCount: 30,
            tailLength: 20,
            targetColors: ['#ffffff', '#69D2E7', '#A7DBD8', '#E0E4CC'],
            avoidColors: ['#FF4E50', '#FC913A', '#F9D423', '#8B0000'],
            orbColor: '#ffffff',
            maxLight: 100,
            lightDecayRate: 0.03, 
            damagePerHit: 15,
            healPerHit: 8,
            negativeBurstThreshold: 3
        };

        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const timerEl = document.getElementById('timer-display');
        const lightBarEl = document.getElementById('light-bar');
        const lightBarContainer = document.getElementById('light-bar-container');
        const startScreen = document.getElementById('start-screen');
        const gameOverScreen = document.getElementById('game-over-screen');
        const finalTimeEl = document.getElementById('final-time');
        const vignette = document.getElementById('vignette');
        const soundBtn = document.getElementById('sound-btn');
        
        let width, height;
        let gameRunning = false;
        
        let lightLevel = 100;
        let startTime = 0;
        let elapsedTime = 0; 
        let consecutiveRedHits = 0;
        let difficultyFactor = 0; 

        let audioCtx;
        let isMuted = false;
        let masterGain;

        function initAudio() {
            if (audioCtx) return; 
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
            masterGain = audioCtx.createGain();
            masterGain.gain.setValueAtTime(1, audioCtx.currentTime);
            masterGain.connect(audioCtx.destination);
        }

        function playSound(type) {
            if (isMuted || !audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            const panner = audioCtx.createStereoPanner();
            panner.pan.value = (Math.random() * 2) - 1;

            osc.connect(gainNode);
            gainNode.connect(panner);
            panner.connect(masterGain); 

            const now = audioCtx.currentTime;

            if (type === 'good') {
                const notes = [528, 660, 792, 1056]; 
                const freq = notes[Math.floor(Math.random() * notes.length)];
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now);
                gainNode.gain.setValueAtTime(0, now);
                gainNode.gain.linearRampToValueAtTime(0.1, now + 0.05);
                gainNode.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
                osc.start(now);
                osc.stop(now + 1.5);
            } else if (type === 'bad') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(100, now);
                osc.frequency.exponentialRampToValueAtTime(30, now + 0.3);
                gainNode.gain.setValueAtTime(0.1, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc.start(now);
                osc.stop(now + 0.3);
            } else if (type === 'burst') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(80, now);
                osc.frequency.exponentialRampToValueAtTime(10, now + 1.5);
                gainNode.gain.setValueAtTime(0.15, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 1.5);
                osc.start(now);
                osc.stop(now + 1.5);
            }
        }

        function toggleMute() {
            isMuted = !isMuted;
            if (isMuted) {
                soundBtn.innerText = '🔇';
                soundBtn.style.opacity = '0.5';
                if(masterGain) masterGain.gain.setValueAtTime(0, audioCtx.currentTime);
            } else {
                soundBtn.innerText = '🔊';
                soundBtn.style.opacity = '1';
                if (audioCtx && audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
                if(masterGain) masterGain.gain.setValueAtTime(1, audioCtx.currentTime);
            }
        }

        const mouse = { x: 0, y: 0, isActive: false };
        const player = { x: 0, y: 0, radius: 15, trail: [] };

        function resize() {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
            
            if (!gameRunning) {
                player.x = width / 2;
                player.y = height / 2;
                mouse.x = width / 2;
                mouse.y = height / 2;
            }
        }
        window.addEventListener('resize', resize);
        resize();

        function handleInput(x, y) {
            mouse.x = x;
            mouse.y = y;
            mouse.isActive = true;
        }

        window.addEventListener('mousemove', e => handleInput(e.clientX, e.clientY));
        
        window.addEventListener('touchmove', e => {
            e.preventDefault();
            handleInput(e.touches[0].clientX, e.touches[0].clientY);
        }, { passive: false });
        
        window.addEventListener('touchstart', e => {
             if (e.target.closest('.pulse-text') || e.target.closest('#sound-btn')) {
                 return; 
             }
             e.preventDefault();
             handleInput(e.touches[0].clientX, e.touches[0].clientY);
        }, { passive: false });

        class Orb {
            constructor() { this.init(true); }

            init(initial = false) {
                if (!initial) {
                    if (Math.random() > 0.5) {
                        this.x = Math.random() > 0.5 ? -20 : width + 20;
                        this.y = Math.random() * height;
                    } else {
                        this.x = Math.random() * width;
                        this.y = Math.random() > 0.5 ? -20 : height + 20;
                    }
                } else {
                    this.x = Math.random() * width;
                    this.y = Math.random() * height;
                }

                this.radius = Math.random() * 4 + 3;
                const redChance = 0.2 + (difficultyFactor * 0.6);
                this.isTarget = Math.random() > redChance; 
                
                if (this.isTarget) {
                    this.color = config.targetColors[Math.floor(Math.random() * config.targetColors.length)];
                } else {
                    this.color = config.avoidColors[Math.floor(Math.random() * config.avoidColors.length)];
                }
                
                const speedBase = 0.5 + (difficultyFactor * 1.5);
                this.vx = (Math.random() - 0.5) * speedBase * 2;
                this.vy = (Math.random() - 0.5) * speedBase * 2;
                this.angle = Math.random() * Math.PI * 2;
            }

            draw() {
                this.angle += 0.05;
                const pulse = Math.sin(this.angle) * 1;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius + pulse, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                
                if (this.isTarget) {
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = this.color;
                } else {
                    ctx.shadowBlur = 5;
                    ctx.shadowColor = 'rgba(255, 0, 0, 0.5)';
                }
                ctx.fill();
                ctx.shadowBlur = 0; 
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.x < -50 || this.x > width + 50 || this.y < -50 || this.y > height + 50) {
                    this.init();
                }
                this.draw();
            }
        }

        class Shockwave {
            constructor(x, y, isNegative) {
                this.x = x;
                this.y = y;
                this.radius = 10;
                this.alpha = 1;
                this.isNegative = isNegative;
                this.lineWidth = isNegative ? 50 : 20; 
            }

            update() {
                this.radius += this.isNegative ? 25 : 15;
                this.alpha -= 0.03;
                if (this.alpha > 0) {
                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                    if (this.isNegative) {
                        ctx.strokeStyle = `rgba(0, 0, 0, ${this.alpha})`;
                        ctx.shadowBlur = 0;
                    } else {
                        ctx.strokeStyle = `rgba(255, 255, 255, ${this.alpha})`;
                        ctx.shadowBlur = 20;
                        ctx.shadowColor = 'white';
                    }
                    ctx.lineWidth = this.lineWidth;
                    ctx.stroke();
                    ctx.restore();
                }
            }
        }

        let orbs = [];
        let shockwaves = [];

        function initGame() {
            orbs = [];
            shockwaves = [];
            for (let i = 0; i < config.particleCount; i++) {
                orbs.push(new Orb());
            }
            lightLevel = 100;
            consecutiveRedHits = 0;
            startTime = Date.now();
            elapsedTime = 0;
            difficultyFactor = 0;
            
            lightBarContainer.style.opacity = '1';
            gameOverScreen.style.display = 'none';
            vignette.style.background = 'radial-gradient(circle, transparent 50%, rgba(0,0,0,0.8) 120%)';
            updateTimer(0);
        }

        function formatTime(ms) {
            const totalSeconds = Math.floor(ms / 1000);
            const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
            const seconds = (totalSeconds % 60).toString().padStart(2, '0');
            return `${minutes}:${seconds}`;
        }

        function updateTimer(ms) {
            timerEl.innerText = formatTime(ms);
        }

        function updateLightBar() {
            const percentage = Math.max(0, Math.min(100, lightLevel));
            lightBarEl.style.width = `${percentage}%`;
            
            if (percentage < 30) {
                lightBarEl.style.background = '#FF4E50';
                lightBarEl.style.boxShadow = '0 0 10px #FF4E50';
            } else {
                lightBarEl.style.background = 'linear-gradient(90deg, #69D2E7, #ffffff)';
                lightBarEl.style.boxShadow = '0 0 10px #ffffff';
            }

            const darkness = 1 - (percentage / 100);
            const center = 50 - (darkness * 30); 
            const edge = 120 - (darkness * 40);
            const opacity = 0.8 + (darkness * 0.2); 
            vignette.style.background = `radial-gradient(circle, transparent ${center}%, rgba(0,0,0,${opacity}) ${edge}%)`;
        }

        function gameOver() {
            gameRunning = false;
            lightBarContainer.style.opacity = '0';
            finalTimeEl.innerText = formatTime(elapsedTime);
            gameOverScreen.style.display = 'flex';
            setTimeout(() => {
                gameOverScreen.style.opacity = '1';
            }, 50);
        }

        function animate() {
            if (!gameRunning) return;

            const now = Date.now();
            elapsedTime = now - startTime;
            updateTimer(elapsedTime);

            difficultyFactor = Math.min(1, elapsedTime / 120000);
            lightLevel -= config.lightDecayRate;

            if (lightLevel <= 0) {
                lightLevel = 0;
                gameOver();
                return; 
            }

            updateLightBar();

            ctx.fillStyle = 'rgba(5, 5, 16, 0.3)';
            ctx.fillRect(0, 0, width, height);

            player.x += (mouse.x - player.x) * 0.1;
            player.y += (mouse.y - player.y) * 0.1;

            player.trail.push({x: player.x, y: player.y});
            if (player.trail.length > config.tailLength) player.trail.shift();

            if (player.trail.length > 1) {
                ctx.beginPath();
                ctx.moveTo(player.trail[0].x, player.trail[0].y);
                for (let i = 1; i < player.trail.length; i++) {
                    ctx.lineTo(player.trail[i].x, player.trail[i].y);
                }
                const trailOpacity = (lightLevel / 100) * 0.5;
                ctx.strokeStyle = `rgba(255, 255, 255, ${trailOpacity})`;
                ctx.lineWidth = player.radius * 0.8;
                ctx.lineCap = 'round';
                ctx.stroke();
            }

            ctx.beginPath();
            ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${lightLevel/100})`; 
            ctx.shadowBlur = lightLevel / 2; 
            ctx.shadowColor = 'white';
            ctx.fill();
            ctx.shadowBlur = 0;

            orbs.forEach(orb => {
                orb.update();
                const dx = player.x - orb.x;
                const dy = player.y - orb.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < player.radius + orb.radius + 10) {
                    handleCollision(orb);
                    orb.init(); 
                }
            });

            shockwaves.forEach((s, index) => {
                if (s.alpha <= 0) shockwaves.splice(index, 1);
                else s.update();
            });

            requestAnimationFrame(animate);
        }

        function handleCollision(orb) {
            if (orb.isTarget) {
                lightLevel = Math.min(config.maxLight, lightLevel + config.healPerHit);
                consecutiveRedHits = 0; 
                shockwaves.push(new Shockwave(player.x, player.y, false));
                playSound('good');
            } else {
                lightLevel -= config.damagePerHit;
                consecutiveRedHits++;
                playSound('bad');
                if (consecutiveRedHits >= config.negativeBurstThreshold) {
                    triggerNegativeBurst();
                }
            }
        }

        function triggerNegativeBurst() {
            consecutiveRedHits = 0;
            lightLevel -= 30; 
            playSound('burst');
            shockwaves.push(new Shockwave(player.x, player.y, true));
            canvas.style.transform = 'translate(5px, 5px)';
            setTimeout(() => canvas.style.transform = 'translate(-5px, -5px)', 50);
            setTimeout(() => canvas.style.transform = 'translate(0, 0)', 100);

            const darkFlash = document.createElement('div');
            darkFlash.style.position = 'absolute';
            darkFlash.style.top = '0';
            darkFlash.style.left = '0';
            darkFlash.style.width = '100%';
            darkFlash.style.height = '100%';
            darkFlash.style.backgroundColor = 'black';
            darkFlash.style.opacity = '0.6';
            darkFlash.style.pointerEvents = 'none';
            darkFlash.style.transition = 'opacity 0.4s';
            darkFlash.style.zIndex = '5';
            document.body.appendChild(darkFlash);
            
            setTimeout(() => {
                darkFlash.style.opacity = '0';
                setTimeout(() => darkFlash.remove(), 400);
            }, 50);
        }

        function startGame() {
            if (gameRunning) return;
            initAudio();
            startScreen.style.opacity = '0';
            setTimeout(() => {
                startScreen.style.display = 'none';
            }, 800);
            gameRunning = true;
            resize(); 
            initGame();
            animate();
        }

        function resetGame() {
            gameOverScreen.style.opacity = '0';
            setTimeout(() => {
                gameOverScreen.style.display = 'none';
                if(masterGain && !isMuted) {
                    masterGain.gain.setValueAtTime(1, audioCtx.currentTime);
                }
                startGame();
            }, 800);
        }
    </script>
</body>
</html>
"""

# 4. HTML Kodunu Streamlit İçinde Çalıştır (Height değerini telefonlara uygun yüksek tutuyoruz)
components.html(html_code, height=900, scrolling=False)
