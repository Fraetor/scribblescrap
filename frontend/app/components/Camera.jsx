import React, { useState, useRef } from 'react';

export default function Camera(setJson) {
    const [image, setImage] = useState(null);
    const inputFile = useRef(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setImage(file);
        // Automatically submit the form when a file is selected
        submitForm(file);
    };

    const submitForm = (file) => {
        console.log("Submitting")
        if (file) {
            console.log("Did the thing!")
            const formData = new FormData();
            formData.append('image', file);

            fetch('/api/create_scribble', {
                method: 'POST',
                body: formData
            })
                .then(response => response.text())
                .then(data => {
                    fetch(`/api/scribble/`+data+"/info", {
                        method: 'GET',
                    })
                    .then(response => response.json())
                    .then(data => setJson(data))
                })
                .catch(error => {
                    // Handle error
                    console.error('Error:', error);
                });
        }
    };

    const onButtonClick = () => {
        inputFile.current.click();
    };

    return (
        <form method="post" encType="multipart/form-data">
            <div>
                <label htmlFor="file">Take Picture</label>
                <input
                    type="file"
                    accept="image/jpeg"
                    id="file"
                    capture="camera"
                    ref={inputFile}
                    style={{ display: 'none' }}
                    onChange={handleFileChange}
                />
            </div>
            <button className="bg-slate-500 p-4 text-black" type="button" onClick={onButtonClick}>Take Picture</button>
        </form>
    );
}
