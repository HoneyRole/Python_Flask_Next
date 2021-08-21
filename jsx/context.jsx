import React, {useContext, useEffect, useState} from "react";
import toast, {Toaster} from 'react-hot-toast'

export const ContextErrorMessage = ({message}) => {
    const context = useContext(AppContext);
    if (!message) {
        return null;
    }
    return (<div
        className="alert alert-danger"
        role="alert">
        <a href="#" title="close" className="close" onClick={() => context.setErrorMessage(null)}
           aria-label="Close"
           aria-hidden="true">&times;</a>
        <span id="flash-message">{message}</span>
    </div>)
}

export const ContextMessage = ({message}) => {
    useEffect(() => {
        if (message) {
            toast.success(message)
        }
    }, [message]);

    return <Toaster toastOptions={{duration: 15000}}/>
}

function useStorage(key, initialValue = null) {
    const [value, setValue] = useState(localStorage.getItem(key) === null || window.g.anon ? initialValue : localStorage.getItem(key));

    function setter(newValue) {
        setValue(newValue);
        localStorage.setItem(key, newValue)
    }

    return [value, setter]
}

export function useContextState() {
    const [message, setMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(window.g_json?.authenticated);
    const [userId, setUserId] = useState(window.g_json?.user?.id);

    return {
        message,
        setMessage,
        errorMessage,
        setErrorMessage,
        authenticated,
        setAuthenticated,
        userId,
        setUserId,
    }
}

export const
    AppContext = React.createContext({});
