import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private login_url = '/auth2/login'; //'http://localhost:5000/auth2/login'
  private session_url =  '/auth2/session'; //'http://localhost:5000/auth/login'
  private logout_url =  '/auth2/logout';
  private register_url = '/auth2/register';

  logged_in: BehaviorSubject<boolean>

  constructor(private http: HttpClient) { 
                this.logged_in = new BehaviorSubject(false)
              }

  login_user(user:any) {
    return this.http.post<any>(this.login_url, user)
  }
  
  register_user(user:any) {
    return this.http.post<any>(this.register_url,user)
  }
  
  session_user() {
    return this.http.post<any>(this.session_url,{})
  }
  
  logout_user() {
    return this.http.post<any>(this.logout_url,{})
  }
  
  logged() {
    this.logged_in.next(true)
  }

  not_logged() {
    this.logged_in.next(false)
  }

  get_email() {
    return localStorage.getItem('user_email')
  }
}
