## name: plot_nrmse_comparison.r
## date: 06/18/2018

library(ggplot2)
library(reshape2)

# color
p_jama=c(
  'Limed Spruce' = '#374E55', 'Anzac'         = '#DF8F44',
  'Cerulean'     = '#00A1D5', 'Apple Blossom' = '#B24745',
  'Acapulco'     = '#79AF97', 'Kimberly'      = '#6A6599',
  'Makara'       = '#80796B')

tbl=NULL
for(i in c(5,8,10,20)){
    x=read.delim(paste0('n',i,'.txt'),header=F)
    x=cbind(percent_missing=paste0(i,'%'),x)
    tbl=rbind(tbl,x)
}
colnames(tbl)[-1]=c('Average','SVM','Lasso','Linear','RF','DMIS')
df=melt(tbl)
colnames(df)=c('percent_missing','Model','NRMSE')

# x=read.delim('avg.txt',header=F)
df1=cbind(percent_missing=unique(tbl[,1]),x1=rep(0,5),x2=rep(6,5),y1=x,y2=x)
colnames(df1)=c('percent_missing','x1','x2','y1','y2')

# tmp_col=c(p_jama[c(1:5)],"black")
# names(tmp_col)=c(colnames(tbl)[-1],"avg_imputation")

p1 = ggplot(df,aes(x=model,y=NRMSE)) +
    facet_wrap(~percent_missing,nrow=1) +
    theme_bw() +
    geom_violin(width=4,aes(fill=model),colour="white",alpha=1,linetype=1,lwd=0.5)+
    scale_fill_manual(values=tmp_col) +
    #stat_summary(fun.y=median, geom="point", aes(shape="Median"), size=2,color="red")+
    geom_boxplot(width=0.2)+
    stat_summary(fun.y=mean, geom="point", aes(shape="Mean"), size=2,color="red")+
    scale_shape_manual("", values=rep(10,13))+
    labs(x="Model",y="NRMSE")+
    theme(axis.line.x = element_line(color="black", size = 0.5))+
    theme(axis.line.y = element_line(color="black", size = 0.5))+
    theme(axis.title.x = element_text(colour="black", size=15))+
    theme(axis.title.y = element_text(colour="black", size=15))+
    theme(axis.text.x = element_text(colour="black",angle = 45, hjust = 1, size=15))+
    theme(axis.text.y = element_text(colour="black",size=15))+
    theme(strip.background = element_blank())+
    theme(strip.text.x = element_text(colour="black", size=15))+
    theme(strip.text.y = element_text(colour="black", size=15))+
    geom_segment(aes(x = x1, y = y1, xend = x2, yend = y2), data = df1)
p1

pdf(file="nrmse_comparison.pdf",width=12,height=6,useDingbats=F)
p1
dev.off()



