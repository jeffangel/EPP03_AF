import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CaseService {

  private new_case_url =  '/report/new';
  private retrieve_cases_url =  '/report/retrieve';

  constructor(private http: HttpClient) { }

  register_case(case_data:any) {
    return this.http.post<any>(this.new_case_url, case_data)
  }

  retrieve_cases(){
    return this.http.get(this.retrieve_cases_url)
  }
}

