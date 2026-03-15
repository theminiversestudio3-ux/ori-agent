const { 
    default: makeWASocket, 
    useMultiFileAuthState, 
    DisconnectReason,
    Browsers,
    fetchLatestBaileysVersion
} = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const pino = require('pino');

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    const { version, isLatest } = await fetchLatestBaileysVersion();
    console.log(`Using WA version v${version.join('.')}, isLatest: ${isLatest}`);
    
    const sock = makeWASocket({
        version,
        auth: state,
        browser: Browsers.ubuntu('Chrome'),
        logger: pino({ level: 'silent' }),
        generateHighQualityLinkPreview: true,
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if(qr) {
            qrcode.generate(qr, { small: true });
        }

        if(connection === 'close') {
            const shouldReconnect = (lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut);
            console.log('connection closed due to ', lastDisconnect.error, ', reconnecting ', shouldReconnect);
            if(shouldReconnect) {
                console.log('Waiting 10 seconds before reconnecting...');
                setTimeout(() => connectToWhatsApp(), 10000);
            }
        }
 else if(connection === 'open') {
            console.log('opened connection');
        }
    });

    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if(type !== 'notify') return;
        
        const msg = messages[0];
        if(!msg.message || msg.key.fromMe) return;

        const jid = msg.key.remoteJid;
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text;

        if(!text) return;

        console.log(`Received from ${jid}: ${text}`);

        try {
            // Forward to Python Brain
            const response = await axios.post('http://localhost:5000/chat', {
                message: text,
                jid: jid
            });

            const reply = response.data.response;
            
            // Send back to WhatsApp
            await sock.sendMessage(jid, { text: reply });
        } catch (error) {
            console.error('Error contacting Brain:', error.message);
            await sock.sendMessage(jid, { text: "Sorry, I'm having trouble thinking right now. Is my brain (Python) running?" });
        }
    });
}

connectToWhatsApp();
