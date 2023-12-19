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

export async function addEntry({name, polish_file_name, familiarity, english_file_name}) {
    try {
        const response = await fetch(`${API_BASE_URL}/addentry`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                word: name,
                polish_path: polish_file_name,
                familiarity: familiarity,
                english_path: english_file_name
            })
        });
        if (!response.ok) {
            throw new Error("fetch failed");
        }
        return response.json();
    } catch (error) {
        throw new Error(`Error in fetchData: ${error.message}`);
    }
}

export async function removeEntry({polish_path, english_path}) {
    try {
        const response = await fetch(`${API_BASE_URL}/removeentry`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                polish_path: polish_path,
                english_path: english_path
            })
        });
        if (!response.ok) {
            throw new Error("fetch failed");
        }
        return response.json();
    } catch (error) {
        throw new Error(`Error in fetchData: ${error.message}`);
    }
}

export async function generatePodcast({length, familiarity_level, speed, gap, email}) {
    try {
        const response = await fetch(`${API_BASE_URL}/generatepodcast`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                length: length,
                familiarity_level: familiarity_level,
                speed: speed,
                gap: gap,
                email: email
            })
        });
        if (!response.ok) {
            throw new Error("fetch failed");
        }
        return response.json();
    } catch (error) {
        throw new Error(`Error in fetchData: ${error.message}`);
    }
}