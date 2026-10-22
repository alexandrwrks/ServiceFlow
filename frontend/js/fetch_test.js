async function testFetch() {
    try {
        const response = await fetch("/api/health");

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        console.log(data);

    } catch (error) {
        console.error("Ошибка запроса:", error);
    }
}

document
    .querySelector("#fetch-button")
    .addEventListener("click", testFetch);