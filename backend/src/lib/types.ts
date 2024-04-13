import { Types } from "mongoose";

export interface Quest {
  _id: Types.ObjectId;
  waypoints: Waypoint[];
}

export interface Waypoint {
  _id: Types.ObjectId;
  latitude: number;
  longitude: number;
  clue: string;
}
