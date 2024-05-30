export default function SignUp(){

    const [data, setData] = useState({})

    const handleSubmission = () => {
        const {email, password, confirmation} = data;

        if (!email || !password){
            alert("Please fill in all fields.");
            return false;
        }
    
        fetch("http://127.0.0.1:8000/signin/", {
            method: "POST",
            body: JSON.stringify(data),
        }).then(response => response.json())
        then(data => {
            if(!data.access){
                return alert("Couldn't create user.");
            }
            localStorage.setItem("token", data.access);
            window.location.href = "/";
        });
    }

    return (
        <div className="p-5">
            <div>
                <h1>Sign In</h1>
                <input className="form-control" onChange={({target}) => setData(prev => ({...prev, email: target.value}))}/>
                <input className="form-control" onChange={({target}) => setData(prev => ({...prev, password: target.value}))}/>
                <button onClick={handleSubmission} className="btn btn-primary">Submit</button>
            </div>
        </div>
    );
}