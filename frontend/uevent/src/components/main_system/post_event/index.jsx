import React, { useState, useEffect } from 'react';
import { Form, Button, ProgressBar, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from "axios";
import uevent from "../../../image/uevent.png"; // Import the image here
import * as S from "./style";
const FileUploadSection = ({ uploadInput, handleSelectFile, selectedFile }) => (
    <div>
        <div className="mb-3">
            <label htmlFor="file" className="btn btn-primary" style={{ cursor: 'pointer' }}>
                Select poster(s) to upload (optional)
                <input
                    type="file"
                    multiple
                    className="form-control"
                    id="file"
                    ref={uploadInput}
                    onChange={handleSelectFile}
                    style={{ display: 'none' }}
                />
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
    </div>
);

const EventForm = ({
    handleSubmit,
    handleChange,
    eventData,
    clubNames,
    selectedFile,
    uploadInput,
    handleSelectFile,
    isUploading,
    uploadProgress,
    isFileUploaded,
    uploadedFile,
}) => (
    <Form onSubmit={handleSubmit} className="d-flex justify-content-center align-items-center">
        <div className="col-md-8">
            {/* Event Name */}
            <Form.Group controlId="event_name">
                <Form.Label>Event Name</Form.Label>
                <Form.Control type="text" name="event_name" value={eventData.event_name} onChange={handleChange} required />
            </Form.Group>

            {/* Event Time */}
            <Form.Group controlId="event_time">
                <Form.Label>Event Time</Form.Label>
                <Form.Control type="text" name="event_time" value={eventData.event_time} onChange={handleChange} required />
            </Form.Group>

            {/* Event Description */}
            <Form.Group controlId="event_description">
                <Form.Label>Event Description</Form.Label>
                <Form.Control as="textarea" name="event_description" value={eventData.event_description} onChange={handleChange} />
            </Form.Group>

            {/* Address */}
            <Form.Group controlId="address">
                <Form.Label>Address</Form.Label>
                <Form.Control type="text" name="address" value={eventData.address} onChange={handleChange} />
            </Form.Group>

            {/* Fee */}
            <Form.Group controlId="fee">
                <Form.Label>Fee</Form.Label>
                <Form.Control type="text" name="fee" value={eventData.fee} onChange={handleChange} />
            </Form.Group>

            {/* Club Name */}
            <Form.Group controlId="club_name">
                <Form.Label>Club Name</Form.Label>
                <Form.Control as="select" name="club_name" value={eventData.club_name} onChange={handleChange} required>
                    <option value="">Select a club</option>
                    {clubNames.map((club, index) => (
                        <option key={index} value={club}>
                            {club}
                        </option>
                    ))}
                </Form.Control>
            </Form.Group>

            {/* Shared Title */}
            <Form.Group controlId="shared_title">
                <Form.Label>Shared Title</Form.Label>
                <Form.Control type="text" name="shared_title" value={eventData.shared_title} onChange={handleChange} />
            </Form.Group>

            <div className="mb-4" />

            {/* File input and selected file display */}
            <FileUploadSection
                uploadInput={uploadInput}
                handleSelectFile={handleSelectFile}
                selectedFile={selectedFile}
            />

            {/* Upload Progress Section */}
            {isUploading && selectedFile && selectedFile.length > 0 && (
                <div className="mt-3 text-center">
                    <div className="mb-3">Upload Progress</div>
                    <ProgressBar now={uploadProgress} label={`${uploadProgress}%`} />
                </div>
            )}


            {/* Uploaded File Section */}
            {isFileUploaded && uploadedFile && uploadedFile.length > 0 && (
                <div className="mt-4 text-center">
                    <h3 className="text-success mb-3">File(s) uploaded successfully</h3>
                    <div className="bg-azure p-4 rounded">
                        <h5 className="fw-bold">Uploaded file(s)</h5>
                        <div className="d-flex flex-column">
                            {uploadedFile.map((item, index) => (
                                <p key={index}><b>{index + 1}. </b>{item.name}</p>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Submit Button */}
            <S.DivButtons>
                <Button variant="primary" type="submit">
                    Post the event
                </Button>
            </S.DivButtons>
        </div>
    </Form>
);

const PostEventForm = () => {
    const [eventData, setEventData] = useState({
        event_name: '',
        event_time: '',
        event_description: '',
        address: '',
        fee: '',
        shared_title: '',
        club_name: ''
    });
    const [clubNames, setClubNames] = useState([]);
    const [err, seterr] = useState(null);

    const [, setfileURL] = useState("");
    const [selectedFile, setselectedFile] = useState(null);
    const [uploadedFile, setuploadedFile] = useState({});
    const [isUploading, setisUploading] = useState(false);
    const [isFileUploaded, setisFileUploaded] = useState(false);
    const [uploadProgress, setuploadProgress] = useState(0);
    let uploadInput = React.createRef();

    // Fetch club names when the component mounts
    useEffect(() => {
        fetch('https://ece444uevent.pythonanywhere.com/main_sys/allClubs')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => setClubNames(data))
            .catch(error => {
                console.error('Error fetching club names:', error);
            });
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEventData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };
    // Track selected file before the upload
    const handleSelectFile = (e) => {
        const selectedFileList = [];
        for (let i = 0; i < e.target.files.length; i++) {
            selectedFileList.push(e.target.files.item(i));
        }
        setselectedFile(selectedFileList);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setisUploading(true);

        const data = new FormData();

        // Append the file to the request body if a file is selected
        if (selectedFile && selectedFile.length > 0) {
            for (let i = 0; i < selectedFile.length; i++) {
                data.append("file", selectedFile[i], selectedFile[i].name);
            }
        }

        // Append other form data properties
        Object.keys(eventData).forEach((key) => {
            data.append(key, eventData[key]);
        });

        try {
            const config = {
                onUploadProgress: (progressEvent) => {
                    const { loaded, total } = progressEvent;
                    setuploadProgress(Math.round((loaded / total) * 10000));
                },
                headers: {
                    "Content-Type": "multipart/form-data",
                    "Authorization": `${window.localStorage['token']}`,
                    'Access-Control-Allow-Origin': '*',
                },
            };

            const response = await axios.post(
                "https://ece444uevent.pythonanywhere.com/main_sys/add/event",
                data,
                config
            );

            setfileURL(`https://ece444uevent.pythonanywhere.com/${response.data.filename}`);

            // Check if the response status is in the 2xx range
            if (response.status >= 200 && response.status < 300) {
                console.log('Post event successful!');
                setisFileUploaded(true);
                setisUploading(false);
                setuploadedFile(selectedFile);
            } else {
                // Handle other status codes (e.g., 400 Bad Request)
                const errorData = await response.json();
                const code = errorData.code;
                const message = errorData.error || 'Unknown error';
                if (code == "401" & message == "Authentication is required to access this resource") {
                    // Redirect to the homepage or another desired page
                    alert('Please log in to continue.');
                    window.location.href = '/login';
                }
                seterr(`Request failed: ${code} - ${message}`);
                setisUploading(false);
                setisFileUploaded(false);
            }
        } catch (error) {
            setisUploading(false);
            setisFileUploaded(false);
            if (error.response) {
                if (error.response.request.status) {
                    const errorCode = error.response.request.status;
                    const errorMessage = error.response.data.error;
                    seterr(`Bad Request: ${errorCode} - ${errorMessage}`);
                } else if (error.response.data.code) {
                    const errorCode = error.response.data.code;
                    const errorMessage = error.response.request.statusText;
                    seterr(`Bad Request: ${errorCode} - ${errorMessage}`);
                }
            } else if (error.request) {
                seterr('No response received from the server. Please try again later.');
            } else {
                seterr('Error occurred while processing the request. Please try again later.');
            }
        }
    }


    return (
        <div className="container mt-5" >
            <div className="col-md-6 offset-md-3">
                <div className="card">
                    <div className="card-body">
                        <S.Img src={uevent} />
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                            <h3 style={{ marginRight: '10px' }}>New event?</h3>
                            {err && <Alert variant="danger">{err}</Alert>}
                        </div>
                        <EventForm
                            eventData={eventData}
                            handleChange={handleChange}
                            clubNames={clubNames}
                            selectedFile={selectedFile}
                            handleSelectFile={handleSelectFile}
                            handleSubmit={handleSubmit}
                            uploadInput={uploadInput}
                            isUploading={isUploading}
                            uploadProgress={uploadProgress}
                            isFileUploaded={isFileUploaded}
                            uploadedFile={uploadedFile}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PostEventForm;
