export function getRequestHeaders() {
    return {headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
    }}
}

export const baseUrl = "http://127.0.0.1:8000"
