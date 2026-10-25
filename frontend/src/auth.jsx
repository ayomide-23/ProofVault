import { createContext, useContext, useState } from "react";

// auth the determine if a user is logged in or logged out 
const auth = createContext(null);

export function Authprovider({children}){
    const [user, setuser] = useState(() => 
        JSON.parse(localStorage.getItem("pv_user") || null)
    )

    const login = (u) => {
        localStorage.getItem("pv_user", JSON.stringify(u));
        setuser(u);
    }

    const logout = () => {
        localStorage.removeItem("pv_item");
        setuser(null);
    }
    return <auth.Provider value = {{user, login, logout}}>{children}</auth.Provider>
}
export const useauth = () => useContext(auth)
