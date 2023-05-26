
age_scatter <- function(res, pheno, betas, i){

	# extract info
	probe <- rownames(res)[i]													# the i_th probe in res
	betas.plot <- (betas[probe,])*100											# corresponding DNAm values for probe. Multiplied by 100 for %
	age <- pheno[,'PCW'] 														# age column of sample sheet
	data <- data.frame(Betas=betas.plot, Age=age)								# combine DNAm (y-axis) and age (x-axis) into df

	# creating the title using probe ID, gene name (if applicable) and chr
	if(res[i,'Gene']!=''){														# if gene is present...
		ttl <- paste0(probe, ' - ', res[i,'Gene'], ' - CHR ',res[i,'CHR'])			# combine probe ID, gene name and chromosome
	}else{																		# if there's no gene name...
		ttl <- paste0(probe, ' - CHR ', res[i,'CHR'])								# just probe ID and chr
	}
	ttl <- paste0(ttl, "\np = ", signif(res[i,'P.Age'], digits=3))				# append the p-value for that probe to the title as a new line

	# plot
	ggplot(data, aes(x=Age, y=Betas)) + 
		geom_point(size=3)+
		ggtitle(ttl)+
		xlab("Age (PCW)")+
		ylab("DNA methylation (%)")+
		ylim(0,100)+
		stat_smooth(method = lm, formula = y ~ x,se=T) +
		theme_minimal()+
		theme(axis.text=element_text(size=19), axis.title=element_text(size=20))+
		theme(plot.title = element_text(size=21))
}

myplots <- list()
for(i in 1:10){
	p <- age_scatter(res.ord, pheno, betas, i)
	myplots[[i]] <- p
}
