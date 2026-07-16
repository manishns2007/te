import axios from 'axios';
import type { DashboardData, TransactionDetail, Prediction } from '../types';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const DashboardService = {
    getDashboardData: async (): Promise<DashboardData> => {
        const res = await api.get('/dashboard');
        return res.data;
    },
};

export const TransactionService = {
    getTransaction: async (id: string): Promise<TransactionDetail> => {
        const res = await api.get(`/transactions/${id}`);
        return res.data;
    },
};

export const DecisionService = {
    submitDecision: async (id: string, action: string, notes: string) => {
        const res = await api.post(`/transactions/${id}/decision`, { action_taken: action, notes, investigator_id: 'Investigator-1' });
        return res.data;
    },
};

export const PredictionService = {
    repredict: async (id: string): Promise<Prediction> => {
        const res = await api.post(`/transactions/${id}/repredict`);
        return res.data;
    }
}

export default api;
