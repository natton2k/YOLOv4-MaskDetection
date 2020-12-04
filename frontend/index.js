
async function getAllThermalData() {
    return await fetch("http://localhost:8080/").then(res => res.json());
}

async function getLatestThermalData() {
    return await fetch("http://localhost:8080/latest").then(res => res.json());
}

function parseAllThermalDataToTable() {
    return getAllThermalData().then((res) => {
        return res;
    })
}

function parseLatestThermalDataToTable() {
    return getLatestThermalData().then((res) => {
        return res;
    })
}