import React, { useState, useRef } from 'react';

export default function Camera({ setJson }) {
    const [image, setImage] = useState(null);
    const inputFile = useRef(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const maxWidth = 50; // Set your maximum width here
                const maxHeight = 50; // Set your maximum height here
                let width = img.width;
                let height = img.height;
                
                if (width > height) {
                    if (width > maxWidth) {
                        height *= maxWidth / width;
                        width = maxWidth;
                    }
                } else {
                    if (height > maxHeight) {
                        width *= maxHeight / height;
                        height = maxHeight;
                    }
                }
                
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                canvas.toBlob((blob) => {
                    const resizedFile = new File([blob], file.name, {
                        type: 'image/jpeg', // You can adjust the type if needed
                        lastModified: Date.now(),
                    });
                    submitForm(resizedFile);
                }, 'image/jpeg'); // You can adjust the type if needed
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
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
                    .catch()
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
