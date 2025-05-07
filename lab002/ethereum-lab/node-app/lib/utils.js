import fs from 'fs';

export const updateContractsMap = (name, address, chainId = 1337) => {
    const path = './config/contracts-map.json';
    const map = fs.existsSync(path) ? JSON.parse(fs.readFileSync(path)) : {};
    map[chainId] = map[chainId] || {};
    map[chainId][name] = address;
    fs.writeFileSync(path, JSON.stringify(map, null, 2));
    console.log(`📍 ${name} address saved to contracts-map.json`);
};
