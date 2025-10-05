// static/js/notifications.js
class NotificationManager {
    constructor() {
        this.pollInterval = 30000; // 30 seconds
        this.init();
    }

    init() {
        this.loadNotifications();
        this.setupPolling();
        this.setupEventListeners();
    }

    async loadNotifications() {
        try {
            const response = await fetch('/notifications/unread-count/');
            const data = await response.json();
            this.updateNotificationCount(data.count);
            
            // Load recent notifications
            this.loadRecentNotifications();
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }

    async loadRecentNotifications() {
        try {
            const response = await fetch('/notifications/?limit=5');
            const html = await response.text();
            
            // Parse the HTML and extract notification items
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const notifications = doc.querySelectorAll('.list-group-item');
            
            this.renderNotifications(notifications);
        } catch (error) {
            console.error('Error loading recent notifications:', error);
        }
    }

    renderNotifications(notifications) {
        const container = document.getElementById('notificationItems');
        const loader = document.getElementById('notificationLoader');
        
        if (notifications.length === 0) {
            loader.innerHTML = '<div class="text-center py-3"><i class="fas fa-bell-slash text-muted"></i><p class="text-muted mb-0">No notifications</p></div>';
            return;
        }
        
        loader.style.display = 'none';
        container.innerHTML = '';
        
        notifications.forEach(notification => {
            container.appendChild(notification.cloneNode(true));
        });
    }

    updateNotificationCount(count) {
        const badge = document.getElementById('notificationCount');
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
        
        // Update page title
        if (count > 0) {
            document.title = `(${count}) NSSF Attachment Portal`;
        } else {
            document.title = 'NSSF Attachment Portal';
        }
    }

    setupPolling() {
        setInterval(() => {
            this.loadNotifications();
        }, this.pollInterval);
    }

    setupEventListeners() {
        // Mark as read when clicking on notifications
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-mark-as-read]')) {
                e.preventDefault();
                const notificationId = e.target.closest('[data-mark-as-read]').dataset.markAsRead;
                this.markAsRead(notificationId);
            }
        });

        // Refresh notifications when dropdown is shown
        const dropdown = document.getElementById('notificationsDropdown');
        dropdown.addEventListener('show.bs.dropdown', () => {
            this.loadRecentNotifications();
        });
    }

    async markAsRead(notificationId) {
        try {
            await fetch(`/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
            });
            
            this.loadNotifications();
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NotificationManager();
});