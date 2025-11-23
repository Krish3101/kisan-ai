import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response.data,
    (error) => {
        console.error('API Error:', error.response?.data || error.message);
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            // Optional: Redirect to login if not already there
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error.response?.data || error.message);
    }
);

export const authApi = {
    login: (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        return api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
    },
    register: (data) => api.post('/auth/register', data),
    getProfile: () => api.get('/auth/me'),
    logout: () => api.post('/auth/logout'),
};

export const weatherApi = {
    getWeather: (city) => api.get(`/weather?city=${city}`),
    getForecast: (city) => api.get(`/weather/forecast?city=${city}`),
};

export const cropsApi = {
    getAll: () => api.get('/crops'),
    add: (data) => api.post('/crops/add', data),
    delete: (id) => api.post('/crops/delete', { id }),
    updateStage: (id, stage) => api.patch(`/crops/${id}/stage`, { stage }),
};

export const expensesApi = {
    getAll: () => api.get('/expense/list'),
    add: (data) => api.post('/expense/add', data),
    delete: (id) => api.delete(`/expense/${id}`),
    getSummary: () => api.get('/expense/summary'),
};

export const pricesApi = {
    getPrice: (crop, state) => api.get(`/price?crop=${crop}&state=${state}`),
};

export const chatApi = {
    sendMessage: (data) => api.post('/chatbot', data),
};

export const soilApi = {
    getAll: () => api.get('/soil'),
    add: (data) => api.post('/soil/add', data),
};

export const dashboardApi = {
    getInsight: (city = 'Pune', crop = 'Tomato') => api.get(`/dashboard/insight?city=${city}&crop=${crop}`),
};

export default api;
