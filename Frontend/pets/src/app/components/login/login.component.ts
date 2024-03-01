import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

import { first } from 'rxjs/operators';

import { AuthService } from '../../services/auth.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  
  redirect_url: any = ''
  password_incorrect:boolean = false
  user_exists:boolean = true

  constructor(private fb: FormBuilder,
              private authService: AuthService,
              private router: Router,
              private activated_route: ActivatedRoute) { }
  
  login_form = this.fb.group({
    email: ['', [Validators.required]],
    password: ['', [Validators.required]]
  });

  ngOnInit(): void {
    if (localStorage.getItem("user_email")) {
      this.router.navigateByUrl("/")
    }
    this.authService.not_logged()
    this.redirect_url = this.activated_route.snapshot.queryParamMap.get('redirectUrl') || '/'
  }

  login() {
    const user = { CORREO: this.login_form.controls.email.value, CLAVE: this.login_form.controls.password.value }
    console.log(user)
    this.authService.login_user(user).subscribe({
      next: data => {
        console.log(data)
        console.log("respuesta")
        if(data['msg'] == 'login_successfully'){
          /* localStorage.setItem('user_id', 'data.token') */
          console.log(data['msg'])
          this.router.navigateByUrl(this.redirect_url);
          this.authService.logged()
        }
        else if (data['msg'] == 'incorrect_password'){
          this.password_incorrect = true
        }
        else if (data['msg'] == 'user_not_exists'){
          this.user_exists = false
        }
      },
      error: error => {
        console.error('Ocurrió un error: ', error)
        this.router.navigate(['/notfound'])
      }      
    })
  }

  register(){
    this.router.navigate(['/signup'])
  }
}
