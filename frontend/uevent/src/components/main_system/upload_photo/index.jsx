import React, { useState } from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';

function Profile() {
    const [, setfileURL] = useState("");
    const [selectedFile, setselectedFile] = useState(null);
    const [uploadedFile, setuploadedFile] = useState({});
    const [isUploading, setisUploading] = useState(false);
    const [isFileUploaded, setisFileUploaded] = useState(false);
    const [uploadProgress, setuploadProgress] = useState(0);
    const [eventData, setEventData] = useState({
        shared_title: "",
    });

    let uploadInput = React.createRef();

    // Track selected file before the upload
    const handleSelectFile = (e) => {
        const selectedFileList = [];
        for (let i = 0; i < e.target.files.length; i++) {
            selectedFileList.push(e.target.files.item(i));
        }
        setselectedFile(selectedFileList);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEventData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Upload file to server
    const handleUploadFile = async (ev) => {
        ev.preventDefault();

        setisUploading(true);
        const data = new FormData();
        // Append the file to the request body
        for (let i = 0; i < uploadInput.files.length; i++) {
            data.append("file", uploadInput.files[i], uploadInput.files[i].name);
        }

        // Append shared title to the request body
        data.append("shared_title", eventData.shared_title);

        try {
            const config = {
                onUploadProgress: (progressEvent) => {
                    const { loaded, total } = progressEvent;
                    setuploadProgress(Math.round((loaded / total) * 100));
                },
            };
            const response = await axios.post(
                "http://localhost:5000/main_sys/upload",
                data,
                config
            );
            const body = response.data;
            console.log(body);
            setfileURL(`http://localhost:5000/${body.filename}`);
            if (response.status === 200) {
                setisFileUploaded(true); // flag to show the uploaded file
                setisUploading(false);
                setuploadedFile(selectedFile); // set the uploaded file to show the name
            }
        } catch (error) {
            console.error(error);
            setisUploading(false);
        }
    };

    return (
        <div className="container d-flex align-items-center justify-content-center min-vh-100">
            <div className="bg-light p-5 rounded shadow" style={{ width: "800px", height: "600px", overflowY: "auto" }}>
                <h1 className="mb-4 text-center">Image Upload</h1>
                <form onSubmit={handleUploadFile} className="text-center">
                    <div className="mb-3">
                        <label htmlFor="shared_title" className="form-label">Shared Title</label>
                        <input type="text" className="form-control" id="shared_title" name="shared_title" value={eventData.shared_title} onChange={handleChange} />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="file" className="btn btn-primary" style={{ cursor: "pointer" }}>
                            Select file(s) to upload
                            <input type="file" multiple className="form-control" id="file" ref={(ref) => { uploadInput = ref; }} onChange={handleSelectFile} style={{ display: "none" }} />
                        </label>
                    </div>
                    <div className="mb-3">
                        <div className="bg-azure p-4 rounded">
                            <h5 className="fw-bold">Selected file(s)</h5>
                            <div className="d-flex flex-column">
                                {selectedFile && selectedFile.map((item, index) => (
                                    <p key={index}><b>{index + 1}. </b>{item.name}</p>
                                ))}
                            </div>
                        </div>
                    </div>
                    <div className="mb-3 d-flex justify-content-center">
                        <button type="submit" className="btn btn-success" disabled={!selectedFile || isUploading}>
                            Upload
                        </button>
                    </div>
                </form>
                {isUploading && (
                    <div className="mt-3 text-center">
                        <div className="mb-3">Upload Progress</div>
                        <div className="progress">
                            <div className="progress-bar" role="progressbar" style={{ width: `${uploadProgress}%` }} aria-valuenow={uploadProgress} aria-valuemin="0" aria-valuemax="100">{uploadProgress}%</div>
                        </div>
                    </div>
                )}
                {isFileUploaded && (
                    <div className="mt-4 text-center">
                        <h3 className="text-success mb-3">File(s) uploaded successfully</h3>
                        <div className="bg-azure p-4 rounded">
                            <h5 className="fw-bold">Uploaded file(s)</h5>
                            <div className="d-flex flex-column">
                                {uploadedFile && uploadedFile.map((item, index) => (
                                    <p key={index}><b>{index + 1}. </b>{item.name}</p>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Profile;