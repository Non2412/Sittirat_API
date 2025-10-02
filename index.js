const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// CORS middleware
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.sendStatus(200);
    } else {
        next();
    }
});

// Routes
app.get('/', (req, res) => {
    res.json({ 
        message: "Welcome to Sittirat Tourism API",
        version: "1.0.0",
        timestamp: new Date().toISOString(),
        endpoints: [
            "GET / - API information",
            "GET /api/hello - Hello world",
            "GET /api/accommodations - Get accommodations",
            "GET /api/tourists - Get tourists"
        ]
    });
});

app.get('/api/hello', (req, res) => {
    res.json({ 
        message: "Hello from Vercel API",
        timestamp: new Date().toISOString()
    });
});

app.get('/api/accommodations', (req, res) => {
    res.json({
        message: "Accommodations endpoint",
        data: [
            {
                id: 1,
                name: "โรงแรมศรีสะเกษ พาเลซ",
                location: "ศรีสะเกษ",
                price: 1500,
                rating: 4.5
            },
            {
                id: 2,
                name: "รีสอร์ทแก้วกุมภา",
                location: "กันทรลักษ์",
                price: 2000,
                rating: 4.8
            }
        ]
    });
});

app.get('/api/tourists', (req, res) => {
    res.json({
        message: "Tourists endpoint",
        data: [
            {
                id: 1,
                name: "สมชาย ใจดี",
                email: "somchai@example.com",
                phone: "081-234-5678"
            }
        ]
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        error: "Route not found",
        path: req.originalUrl,
        method: req.method
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: "Internal server error",
        message: err.message
    });
});

const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

module.exports = app;