/* ============================================
   FUNCIONALIDADES INTERACTIVAS
   ============================================ */

// ============================================
// TOGGLE MODO OSCURO
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
});

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
}

// ============================================
// SCROLL ANIMATIONS
// ============================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.card, .pregunta-item, .ranking-card').forEach(el => {
    observer.observe(el);
});

// ============================================
// NOTIFICACIONES PERSONALIZADAS
// ============================================
function showNotification(message, type = 'success', duration = 3000) {
    const colors = {
        success: '#00D2A0',
        error: '#FF6B6B',
        warning: '#FFC857',
        info: '#4ECDC4'
    };
    
    const notification = document.createElement('div');
    notification.className = 'notification-custom';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${colors[type] || '#6C63FF'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideInRight 0.5s ease;
        font-weight: 500;
        max-width: 400px;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    }, duration);
}

// Estilos para notificaciones
const styleNotificaciones = document.createElement('style');
styleNotificaciones.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(styleNotificaciones);
