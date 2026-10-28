const Base = import.meta.env.VITE_BACKEND_URL;

async function request(path, options = {}){
     const res = await fetch(`${Base}${path}`, {
        headers: {"Content-Type" : "application/json"},
        ...options,
     })
     const data = await res.json().catch(() => ({}))
     if(!res.ok){
        const detail = Array.isArray(data.detail) ? data.detail[0].msg.replace("Value error,  ", ""): data.detail;
        throw new Error(detail || `Request failed (${res.status})`)
    }
    return data;
}

export const api = {
    login: (phone_number, name) => 
        request("/users/", {method: "POST", body: JSON.stringify({phone_number, name})}),
    create_agreement: (body) => 
        request("/agreements/", {method: "POST", body: JSON.stringify(body)}),
    get_agreement: (id) => request(`/agreements/${id}`),
    list_agreements: (user_id) => request(`/agreements/?user_id=${user_id}`),
    sign: (id, signer_id) => 
        request(`/agreements/${id}/sign`, {method: "POST", body:JSON.stringify({signer_id})})
};