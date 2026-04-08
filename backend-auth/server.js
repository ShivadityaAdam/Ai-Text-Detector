const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { PrismaClient } = require('@prisma/client'); 
const cors = require('cors');

const prisma = new PrismaClient();
const app = express();
const SECRET_KEY = process.env.JWT_SECRET || "super_secure_key";

app.use(express.json());
app.use(cors());


app.post('/api/signup', async (req, res) => {
    const { username, password } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = await prisma.user.create({
            data: { username, password: hashedPassword }
        });
        res.status(201).json({ message: "User Created", userId: user.id });
    } catch (error) {
        res.status(400).json({ error: "Username already exists" });
    }
});

app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await prisma.user.findUnique({ where: { username } });

    if (user && await bcrypt.compare(password, user.password)) {
        const token = jwt.sign({ userId: user.id }, SECRET_KEY, { expiresIn: '24h' });
        res.json({ token });
    } else {
        res.status(401).json({ error: "Invalid Credentials" });
    }
});


app.get('/api/history', async (req, res) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).send("Unauthorized");

    try {
        const decoded = jwt.verify(token, SECRET_KEY);
        const history = await prisma.scan.findMany({
            where: { userId: decoded.userId },
            orderBy: { createdAt: 'desc' }
        });
        res.json(history);
    } catch (err) {
        res.status(401).send("Invalid Token");
    }
});

app.listen(3000, () => console.log("Real Production Server Running on Port 3000"));
