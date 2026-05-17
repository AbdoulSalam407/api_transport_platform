import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Vehicule } from '../models/vehicule.model';
import { PaginatedResponse } from './trajet.service';

@Injectable({ providedIn: 'root' })
export class VehiculeService {
  private readonly API = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getMesVehicules(): Observable<PaginatedResponse<Vehicule> | Vehicule[]> {
    return this.http.get<PaginatedResponse<Vehicule> | Vehicule[]>(
      `${this.API}/vehicules/vehicules/`,
    );
  }
}
