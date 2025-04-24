const container = document.getElementById('joystick-container');
const manager = nipplejs.create({
    zone: container,
    mode: 'static',
    position: { left: '50%', top: '50%' },
    color: 'blue',
    size: 200
});

function sendCommand(direction, speed) {
    const form = new FormData();
    form.append('direction', direction);
    form.append('speed', speed);

    fetch('/send', {
        method: 'POST',
        body: form
    }).catch(err => console.error('Command error:', err));
}

manager.on('move', (evt, data) => {
    if (!data || !data.direction) return;

    const dir = data.direction.angle;
    let command = 'S';
    let speed = Math.min(Math.floor(data.distance * 10), 500);

    if (dir === 'up') command = 'F';
    else if (dir === 'down') command = 'B';
    else if (dir === 'left') command = 'L';
    else if (dir === 'right') command = 'R';

    sendCommand(command, speed);
});

manager.on('end', () => {
    sendCommand('S', 0);
});