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

export async function getAudioList() {
    try {
        const response = await fetch(`${API_BASE_URL}/audiolist`, {
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

// export async function addEntry({name, polish_file_name, familiarity, english_file_name, translated_word}) {
//     try {
//         const response = await fetch(`${API_BASE_URL}/addentry`, {
//             method: "POST",
//             mode:"cors",
//             headers: {
//               "Content-Type": "application/json"
//             },
//             body: JSON.stringify({
//                 word: name,
//                 polish_path: polish_file_name,
//                 familiarity: familiarity,
//                 english_path: english_file_name,
//                 translated_word: translated_word
//             })
//         });
//         if (!response.ok) {
//             throw new Error("fetch failed");
//         }
//         return response.json();
//     } catch (error) {
//         throw new Error(`Error in fetchData: ${error.message}`);
//     }
// }

export async function removeEntry({translated_path, original_path}) {
    try {
        const response = await fetch(`${API_BASE_URL}/removeentry`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                translated_path: translated_path,
                original_path: original_path
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

export async function generatePodcast({length, familiarity_level, speed, gap, percent, percent_orig}) {
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
                percent: percent,
                percent_orig: percent_orig
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

export async function updateFamLevel({id, familiarity_level}) {
    try {
        const response = await fetch(`${API_BASE_URL}/updatefamlevel`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: id,
                familiarity: familiarity_level,
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

export async function updateKnown({id, known}) {
    try {
        const response = await fetch(`${API_BASE_URL}/updateknown`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: id,
                known: known,
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

export async function getAudio({word}) {
    try {
        const response = await fetch(`${API_BASE_URL}/getaudio`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                word: word,
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

export async function removeAudio({path}) {
    try {
        const response = await fetch(`${API_BASE_URL}/removeaudio`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                path: path,
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

export async function submitWord({word, path, familiarity}) {
    try {
        const response = await fetch(`${API_BASE_URL}/submitword`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                word: word,
                path: path,
                familiarity: familiarity
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

export async function generatePhrase() {
    try {
        const response = await fetch(`${API_BASE_URL}/generatephrase`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
        });
        if (!response.ok) {
            throw new Error("fetch failed");
        }
        return response.json();
    } catch (error) {
        throw new Error(`Error in fetchData: ${error.message}`);
    }
}

export async function getPodcastList() {
    try {
        const response = await fetch(`${API_BASE_URL}/podcastlist`, {
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

export async function removePodcastEntry({id}) {
    try {
        const response = await fetch(`${API_BASE_URL}/removepodcastentry`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: id
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

export async function updateListenedStatus({id, listened}) {
    try {
        const response = await fetch(`${API_BASE_URL}/updatelistenedstatus`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: id,
                listened: listened,
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

export async function submitManualWord({original_word, translated_word, familiarity}) {
    try {
        const response = await fetch(`${API_BASE_URL}/submitmanualword`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                original_word: original_word,
                translated_word: translated_word,
                familiarity: familiarity
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

export async function getFreqWords({freq}) {
    try {
        const response = await fetch(`${API_BASE_URL}/getfreqwords`, {
            method: "POST",
            mode:"cors",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                freq: freq
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

export async function uploadGrammarAudio({description, blob}) {
    try {
        const formData = new FormData();
        formData.append("description", description);
        formData.append("blob", blob);
        const response = await fetch(`${API_BASE_URL}/addrecordedaudio`, {
            method: "POST",
            mode:"cors",
            body: formData,
        });
        if (!response.ok) {
            throw new Error("fetch failed");
        }
        return response.json();
    } catch (error) {
        throw new Error(`Error in fetchData: ${error.message}`);
    }
}