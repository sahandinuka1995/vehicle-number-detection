/**
 * @author Sahan Dinuka
 * @CreatedBy IntelliJ IDEA
 * @created 15/12/2021 - 9:57 PM
 */
import React, {Component, useCallback} from 'react';
import {Button, Grid} from '@mui/material';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Icon from "@mui/material/Icon";
import {strings} from "../../const/strings";
import MDButton from "../../components/MDButton";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import {addVehicle} from '../../services/vehicle'
import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
import '../../scss/style.scss'

export default class AddVehicle extends Component {

    state = {
        open: false,
        vehicleNo: '',
        model: '',
        colour: '',
        type: '',
        src: null,
        crop: {
            unit: '%',
            width: 30,
            aspect: 16 / 9
        },
        isCropped: false
    }

    handleClickOpen = (state) => {
        this.setState({
            open: state,
            isCropped: false,
            src: state === false ? null : this.state.src,
            croppedImageUrl: state === false ? null : this.state.croppedImageUrl,
        })
    };

    onInputHandler = (e) => {
        let val = e.target.value

        this.setState({
            [e.target.name]: val
        })
    }

    onSubmit = async () => {
        let state = this.state
        let data = {
            name: 'Sahan',
            vehicleNo: state.vehicleNo,
            model: state.model,
            colour: state.colour,
            type: state.type
        }

        await addVehicle(data).then((res) => {
            if (res.data.success) {
                this.props.loadAll()
                this.handleClickOpen(false)
            }
        })
    }

    onSelectFile = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const reader = new FileReader();
            reader.addEventListener('load', () =>
                this.setState({src: reader.result})
            );
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    onImageLoaded = (image) => {
        this.imageRef = image;
    };

    onCropComplete = (crop) => {
        this.makeClientCrop(crop);
    };

    onCropChange = (crop, percentCrop) => {
        // You could also use percentCrop:
        // this.setState({ crop: percentCrop });
        this.setState({crop});
    };

    async makeClientCrop(crop) {
        if (this.imageRef && crop.width && crop.height) {
            const croppedImageUrl = await this.getCroppedImg(
                this.imageRef,
                crop,
                'newFile.jpeg'
            );
            this.setState({croppedImageUrl});
        }
    }

    getCroppedImg(image, crop, fileName) {
        const canvas = document.createElement('canvas');
        const pixelRatio = window.devicePixelRatio;
        const scaleX = image.naturalWidth / image.width;
        const scaleY = image.naturalHeight / image.height;
        const ctx = canvas.getContext('2d');

        canvas.width = crop.width * pixelRatio * scaleX;
        canvas.height = crop.height * pixelRatio * scaleY;

        ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        ctx.imageSmoothingQuality = 'high';

        ctx.drawImage(
            image,
            crop.x * scaleX,
            crop.y * scaleY,
            crop.width * scaleX,
            crop.height * scaleY,
            0,
            0,
            crop.width * scaleX,
            crop.height * scaleY
        );

        return new Promise((resolve, reject) => {
            canvas.toBlob(
                (blob) => {
                    if (!blob) {
                        //reject(new Error('Canvas is empty'));
                        console.error('Canvas is empty');
                        return;
                    }
                    blob.name = fileName;
                    window.URL.revokeObjectURL(this.fileUrl);
                    this.fileUrl = window.URL.createObjectURL(blob);
                    resolve(this.fileUrl);
                },
                'image/jpeg',
                1
            );
        });
    }


    render() {
        const {crop, croppedImageUrl, src} = this.state;

        return (
            <div>
                <MDButton variant="gradient" color="dark" onClick={() => this.handleClickOpen(true)}>
                    <Icon sx={{fontWeight: "bold"}}>add</Icon>
                    &nbsp;{strings.addNewVehicle}
                </MDButton>
                <Dialog open={this.state.open} onClose={() => this.handleClickOpen(false)} maxWidth={'sm'}
                        fullWidth={true}>
                    <DialogTitle>{strings.addNewVehicle}</DialogTitle>
                    <DialogContent>
                        <Grid container spacing={2}>
                            {!this.state.isCropped ? <Grid item md={12}>
                                    <div className="App">
                                        <div>
                                            <div>
                                                <input type="file" accept="image/*" onChange={this.onSelectFile}/>
                                            </div>
                                            {src && (
                                                <ReactCrop
                                                    src={src}
                                                    crop={crop}
                                                    ruleOfThirds
                                                    onImageLoaded={this.onImageLoaded}
                                                    onComplete={this.onCropComplete}
                                                    onChange={this.onCropChange}
                                                />
                                            )}
                                        </div>
                                        {croppedImageUrl && (
                                            <div align={'center'}>
                                                <img alt="Crop" style={{maxWidth: '100%'}} src={croppedImageUrl}/>
                                            </div>
                                        )}
                                    </div>
                                </Grid> :
                                <>
                                    <Grid item md={6}>
                                        <TextField
                                            autoFocus
                                            margin="dense"
                                            id="name"
                                            label={strings.vehicleNo}
                                            type="text"
                                            fullWidth
                                            variant="standard"
                                            onChange={this.onInputHandler}
                                            name={'vehicleNo'}
                                        />
                                    </Grid>
                                    <Grid item md={6}>
                                        <TextField
                                            autoFocus
                                            margin="dense"
                                            id="name"
                                            label={strings.model}
                                            type="text"
                                            fullWidth
                                            variant="standard"
                                            onChange={this.onInputHandler}
                                            name={'model'}
                                        />
                                    </Grid>
                                    <Grid item md={6}>
                                        <TextField
                                            autoFocus
                                            margin="dense"
                                            id="name"
                                            label={strings.colour}
                                            type="text"
                                            fullWidth
                                            variant="standard"
                                            onChange={this.onInputHandler}
                                            name={'colour'}
                                        />
                                    </Grid>
                                    <Grid item md={6}>
                                        <Box sx={{minWidth: 120}} style={{marginTop: 15}}>
                                            <FormControl fullWidth>
                                                <InputLabel id="demo-simple-select-label">Type</InputLabel>
                                                <Select
                                                    labelId="demo-simple-select-label"
                                                    id="demo-simple-select"
                                                    label="Age"
                                                    onChange={this.onInputHandler}
                                                    style={{height: 40}}
                                                    name={'type'}
                                                >
                                                    <MenuItem value={'BIKE'}>Bike</MenuItem>
                                                    <MenuItem value={'THREE_WHEEL'}>Three Wheel</MenuItem>
                                                    <MenuItem value={'CAR'}>Car</MenuItem>
                                                    <MenuItem value={'VAN'}>Van</MenuItem>
                                                    <MenuItem value={'BUS'}>Bus</MenuItem>
                                                    <MenuItem value={'LORRY'}>Lorry</MenuItem>
                                                    <MenuItem value={'TIPER'}>Tiper</MenuItem>
                                                </Select>
                                            </FormControl>
                                        </Box>
                                    </Grid>
                                </>
                            }

                        </Grid>
                    </DialogContent>
                    <DialogActions>

                        {this.state.isCropped ?
                            <>
                                <Button onClick={() => this.setState({isCropped: false})}>Back</Button>
                                <Button onClick={this.onSubmit}>Save</Button>
                            </> :
                            <>
                                <Button onClick={() => this.handleClickOpen(false)}>Cancel</Button>
                                <Button onClick={() => this.setState({isCropped: true})}>Next</Button>
                            </>}
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}
