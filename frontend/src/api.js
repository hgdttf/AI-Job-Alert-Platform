import axios from "axios";

const API = axios.create({
baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    "https://jobpulse-hghkebgcafc5erda.eastus-01.azurewebsites.net",
headers: {
    "Content-Type": "application/json",
},
timeout: 15000,
});

export default API;