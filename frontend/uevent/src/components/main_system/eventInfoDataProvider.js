class EventInfoDataProvider {
    constructor(eventId, eventName, eventTime, averageRating, eventImage, filterInfo) {
        this._eventId = eventId;
        this._eventName = eventName;
        this._eventTime = eventTime;
        this._averageRating = averageRating;
        this._eventImage = eventImage;
        this._filterInfo = filterInfo
    }

    get filterInfo() {
        return this._filterInfo;
    }

    set filterInfo(value) {
        this._filterInfo = value;
    }

    get eventId() {
        return this._eventId;
    }

    set eventId(value) {
        this._eventId = value;
    }

    get eventImage() {
        return this._eventImage;
    }

    set eventImage(value) {
        this._eventImage = value;
    }

    get eventName() {
        return this._eventName;
    }

    set eventName(value) {
        this._eventName = value;
    }

    get eventDescription() {
        return this._eventDescription;
    }

    set eventDescription(value) {
        this._eventDescription = value;
    }

    get eventTime() {
        return this._eventTime;
    }

    set eventTime(value) {
        this._eventTime = value;
    }

    get averageRating() {
        return this._averageRating;
    }

    set averageRating(value) {
        this._averageRating = value;
    }

    get numberRater() {
        return this._numberRater;
    }

    set numberRater(value) {
        this._numberRater = value;
    }
}

export default EventInfoDataProvider;


