
// Create animated background bubbles
function createBubbles() {
    const background = document.getElementById('background');
    const bubbleCount = 15;
    
    for (let i = 0; i < bubbleCount; i++) {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        
        // Random size between 50px and 200px
        const size = Math.random() * 150 + 50;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        
        // Random position
        bubble.style.top = `${Math.random() * 100}%`;
        bubble.style.left = `${Math.random() * 100}%`;
        
        // Random animation delay
        bubble.style.animationDelay = `${Math.random() * 5}s`;
        
        background.appendChild(bubble);
    }
}

// Popup functionality
function setupPopups() {
    const buttons = {
        intro: document.getElementById('introBtn'),
        skills: document.getElementById('skillsBtn'),
        contact: document.getElementById('contactBtn')
    };
    
    const popups = {
        intro: document.getElementById('introPopup'),
        skills: document.getElementById('skillsPopup'),
        contact: document.getElementById('contactPopup')
    };
    
    // Open popups
    buttons.intro.addEventListener('click', () => {
        popups.intro.classList.add('active');
    });
    
    buttons.skills.addEventListener('click', () => {
        popups.skills.classList.add('active');
    });
    
    buttons.contact.addEventListener('click', () => {
        popups.contact.classList.add('active');
    });
    
    // Close popups
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const popup = button.closest('.popup-container');
            popup.classList.remove('active');
        });
    });
    
    // Close popup when clicking outside
    document.querySelectorAll('.popup-container').forEach(container => {
        container.addEventListener('click', (e) => {
            if (e.target === container) {
                container.classList.remove('active');
            }
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    createBubbles();
    setupPopups();
});
