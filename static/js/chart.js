// static/js/chart.js
// Chart.js integration for dashboard analytics
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the dashboard page
    if (document.getElementById('dashboard-stats')) {
        // You would typically fetch this data from an API endpoint
        // For now, we'll use mock data
        initDashboardCharts();
    }
});

function initDashboardCharts() {
    // Example chart initialization
    const ctx = document.getElementById('attachmentStatusChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Approved', 'Rejected', 'Completed'],
                datasets: [{
                    data: [12, 19, 3, 5],
                    backgroundColor: [
                        '#ffc107',
                        '#198754',
                        '#dc3545',
                        '#0dcaf0'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Attachment Status Distribution'
                    }
                }
            }
        });
    }
    
    // Monthly attachments chart
    const monthlyCtx = document.getElementById('monthlyAttachmentsChart');
    if (monthlyCtx) {
        new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: '# of Attachments',
                    data: [12, 19, 15, 17, 22, 19],
                    backgroundColor: '#1B5E20',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Monthly Attachments'
                    }
                }
            }
        });
    }
}