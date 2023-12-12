const API_BASE_URL = "http://127.0.0.1:5000";

export async function helloWorld() {
    try {
        const response = await fetch(`${API_BASE_URL}/test`, {
            method: "GET",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            }
        });
        if (!response.ok) {
            throw new Error("fetch failed");
        }
        return response.json();
    } catch (error) {
        throw new Error(`Error in fetchData: ${error.message}`);
    }
}